import math
import torch
import numpy as np

class Node:
    def __init__(self, state_emb, prior_prob, parent=None, action_idx=None):
        self.state_emb = state_emb     # Latent vector from World Model
        self.prior_prob = prior_prob   # P from Policy Network
        self.parent = parent
        self.action_idx = action_idx   # The macro action that led here
        
        self.children = {}             # action_idx -> Node
        self.visit_count = 0           # N
        self.value_sum = 0.0           # W
        
    @property
    def q_value(self):                 # Q = W / N
        if self.visit_count == 0:
            return 0.0
        return self.value_sum / self.visit_count

    def to_dict(self):
        # Recursively serialize the node for TUI rendering
        children_dict = {
            int(act): child.to_dict() 
            for act, child in self.children.items() 
            if child.visit_count > 0
        }
        return {
            "n": self.visit_count,
            "q": round(self.q_value, 4),
            "p": round(float(self.prior_prob), 4),
            "c": children_dict
        }
        
    def expand(self, action_probs, next_state_embs):
        """
        Populate children with prior probabilities and exact latent states.
        action_probs: Tensor of shape (num_actions,)
        next_state_embs: Tensor of shape (num_actions, hidden_dim)
        """
        for a_idx, prob in enumerate(action_probs):
            if prob > 1e-6: # Only expand plausible actions
                self.children[a_idx] = Node(
                    state_emb=next_state_embs[a_idx].clone().detach(),
                    prior_prob=prob.item(),
                    parent=self,
                    action_idx=a_idx
                )
                
    def is_expanded(self):
        return len(self.children) > 0


class MCTS:
    def __init__(self, agent, num_simulations=800, c_puct=1.5, num_macros=15):
        self.agent = agent               # HierarchicalMultiAgent 
        self.num_sim_max = num_simulations
        self.c_puct = c_puct
        self.num_macros = num_macros
        self.terminate_action = num_macros - 1
        
    def search(self, root_graph, device='cpu'):
        """
        Runs MCTS simulations from the root physical state.
        root_graph: PyG Data object of the current LLVM code
        Returns: The MCTS policy (visit counts for each action at root)
        """
        import os
        import json
        
        x = root_graph.x.to(device)
        edge_index = root_graph.edge_index.to(device)
        edge_attr = getattr(root_graph, 'edge_attr', None)
        if edge_attr is not None: edge_attr = edge_attr.to(device)
        batch_vec = torch.zeros(x.size(0), dtype=torch.long, device=device)
        
        with torch.no_grad():
            # 1. Evaluate root using World Model Encoder -> Latent State
            root_emb = self.agent.encoder(x, edge_index, batch_vec, edge_type=edge_attr)
            
            # 2. Get Root Policy
            root_probs, _ = self.agent.manager.forward_latent(root_emb)
            root_probs = torch.softmax(root_probs.squeeze(0), dim=-1)
            
        root = Node(state_emb=root_emb.clone(), prior_prob=1.0)
        
        # We need to simulate the Next States for all possible actions from root to expand it.
        # This requires broadcasting the root embedding and running the World Model Dynamics.
        with torch.no_grad():
            batch_root_emb = root_emb.repeat(self.num_macros, 1)
            action_tensor = torch.arange(self.num_macros, device=device)
            # Predict next latent state using the transition model from WorldModel
            if hasattr(self.agent.manager.world_model, 'transition'):
               next_state_embs, _ = self.agent.manager.world_model.transition(batch_root_emb, action_tensor)
            else:
               # Fallback if internal architecture differs slightly:
               action_tensor_unsqueeze = action_tensor.unsqueeze(-1)
               batch_x = x.repeat(self.num_macros, 1)
               _, _, next_state_embs = self.agent.world_model(
                   batch_x, edge_index, batch_vec.repeat(self.num_macros), 
                   action_tensor_unsqueeze, edge_attr=edge_attr
               )

        # Expand root
        root.expand(root_probs, next_state_embs)
        
        # Add Dirichlet noise to root for exploration (AlphaZero trick)
        noise = np.random.dirichlet([0.3] * self.num_macros)
        for a_idx, child in root.children.items():
            child.prior_prob = 0.75 * child.prior_prob + 0.25 * noise[a_idx]
            
        # Run Simulations
        for sim in range(self.num_sim_max):
            node = root
            search_path = [node]
            
            # 1. SELECT (PUCT)
            while node.is_expanded():
                # Find best child using PUCT
                best_action, best_child = self._select_child(node)
                node = best_child
                search_path.append(node)
                
                # Terminal state in simulation (We picked STOP)
                if node.action_idx == self.terminate_action:
                    break
                    
            # 2. EVALUATE & EXPAND
            value = 0.0
            if node.action_idx != self.terminate_action:
                with torch.no_grad():
                    # For Antigravity v4, the critic needs history_emb. We assume 0 for rollout.
                    history_emb = torch.zeros(1, 32, device=device)
                    critic_input = torch.cat([node.state_emb.unsqueeze(0), history_emb], dim=-1)
                    value = self.agent.critic(critic_input).item()
                    
                    # Predict next policy
                    policy_logits, _ = self.agent.manager.forward_latent(node.state_emb.unsqueeze(0))
                    action_probs = torch.softmax(policy_logits.squeeze(0), dim=-1)
                    
                    # Predict next states using World Model
                    batch_node_emb = node.state_emb.repeat(self.num_macros, 1)
                    action_tensor = torch.arange(self.num_macros, device=device)
                    
                    if hasattr(self.agent.manager.world_model, 'transition'):
                        next_state_embs, _ = self.agent.manager.world_model.transition(batch_node_emb, action_tensor)
                    else:
                        next_state_embs = batch_node_emb # Placeholder if transition fails
                        
                node.expand(action_probs, next_state_embs)
            else:
                # If we stopped, the value is whatever we locked in + penalty avoidance
                value = 0.5 
                
            # 3. BACKUP
            self._backpropagate(search_path, value)

        # Extract the visit distribution (MCTS Target Policy)
        visit_counts = np.zeros(self.num_macros)
        for a_idx, child in root.children.items():
            visit_counts[a_idx] = child.visit_count
            
        # Softmax over counts for the final policy output
        if visit_counts.sum() == 0:
            mcts_policy = np.ones(self.num_macros) / self.num_macros
        else:
            mcts_policy = visit_counts / visit_counts.sum()
            
        return mcts_policy, root
        
        
    def _select_child(self, node):
        best_score = -float('inf')
        best_action = -1
        best_child = None
        
        for action_idx, child in node.children.items():
            # PUCT Formula: Q(s,a) + c_puct * P(s,a) * sqrt(N(s)) / (1 + N(s,a))
            u = self.c_puct * child.prior_prob * math.sqrt(node.visit_count) / (1 + child.visit_count)
            q = child.q_value
            score = q + u
            
            if score > best_score:
                best_score = score
                best_action = action_idx
                best_child = child
                
        return best_action, best_child
        
    def _backpropagate(self, search_path, value):
        for node in reversed(search_path):
            node.value_sum += value
            node.visit_count += 1

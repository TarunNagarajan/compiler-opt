import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple

class SpecialistAgent(nn.Module):
    def __init__(self, input_dim, num_macros, hidden_dim=256):
        super(SpecialistAgent, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.LeakyReLU(0.2),
            nn.Linear(hidden_dim, hidden_dim)
        )
        self.action_head = nn.Linear(hidden_dim, num_macros)
        self.conviction_head = nn.Linear(hidden_dim, 1)

    def forward(self, specialist_input):
        feat = self.net(specialist_input)
        probs = F.softmax(self.action_head(feat), dim=-1)
        conviction = torch.sigmoid(self.conviction_head(feat))
        return probs, conviction

class NegotiationModule(nn.Module):
    """
    World-Model Informed Negotiation Module.
    Mediates between 4 specialists by simulating their proposals first.
    Specialists now receive state_emb + history_emb for temporal awareness.
    """
    def __init__(self, state_dim, num_macros, world_model, history_dim=32, action_offset=0):
        super(NegotiationModule, self).__init__()
        self.num_macros = num_macros
        self.world_model = world_model
        self.history_dim = history_dim
        self.action_offset = action_offset
        
        # Specialists see state + history (temporal awareness)
        specialist_input_dim = state_dim + history_dim
        self.performance_agent = SpecialistAgent(specialist_input_dim, num_macros)
        self.speed_agent = SpecialistAgent(specialist_input_dim, num_macros)
        self.size_agent = SpecialistAgent(specialist_input_dim, num_macros)
        self.security_agent = SpecialistAgent(specialist_input_dim, num_macros)
        
        # Simulation Evaluator: State + History + (4 agents * 6 metrics)
        self.mediator = nn.Sequential(
            nn.Linear(state_dim + history_dim + 24, 256),
            nn.ReLU(),
            nn.Linear(256, 4),
            nn.Softmax(dim=-1)
        )

    def forward(self, x, edge_index, batch, state_emb, edge_attr=None, history_emb=None, graph_data=None):
        # Default to zero history if not provided (e.g. PPO recomputation)
        if history_emb is None:
            history_emb = torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        
        # Specialists see both code structure AND pass history
        specialist_input = torch.cat([state_emb, history_emb], dim=-1)
        
        # 1. Generate Proposals (now history-aware)
        p_probs, _ = self.performance_agent(specialist_input)
        v_probs, _ = self.speed_agent(specialist_input)
        s_probs, _ = self.size_agent(specialist_input)
        x_probs, _ = self.security_agent(specialist_input)
        
        # Sample most likely action for each agent to simulate
        p_act = torch.argmax(p_probs, dim=-1)
        v_act = torch.argmax(v_probs, dim=-1)
        s_act = torch.argmax(s_probs, dim=-1)
        x_act = torch.argmax(x_probs, dim=-1)
        
        # 2. Simulation Phase (Using v8 Calibrated transition_step)
        batch_size = state_emb.size(0)
        action_dim = self.world_model.action_dim
        
        # Phase 5: Scale-Aware Simulations
        # Extract total_nodes from graph_data (GSI Signal)
        total_nodes = getattr(graph_data, 'total_nodes', None) if graph_data else None
        if batch is not None:
            _, counts = torch.unique(batch, return_counts=True)
            local_nodes = torch.clamp(counts - 1, min=1).to(device=state_emb.device, dtype=torch.float32)
        else:
            local_nodes = torch.tensor([max(int(x.size(0)) - 1, 1)], dtype=torch.float32, device=state_emb.device)
        
        def make_onehot(act):
            real_act = act + self.action_offset
            oh = torch.zeros(batch_size, action_dim, device=state_emb.device)
            oh.scatter_(1, real_act.view(-1, 1), 1.0)
            return oh
        
        # V8 Refinement: Passing total_nodes so the Manager feels the "Industrial Gravity"
        # during internal reward simulations.
        _, p_metrics = self.world_model.transition_step(state_emb, make_onehot(p_act), num_nodes=local_nodes, total_nodes=total_nodes)
        _, v_metrics = self.world_model.transition_step(state_emb, make_onehot(v_act), num_nodes=local_nodes, total_nodes=total_nodes)
        _, s_metrics = self.world_model.transition_step(state_emb, make_onehot(s_act), num_nodes=local_nodes, total_nodes=total_nodes)
        _, x_metrics = self.world_model.transition_step(state_emb, make_onehot(x_act), num_nodes=local_nodes, total_nodes=total_nodes)
            
        # 3. Mediation Phase (also history-aware)
        sim_input = torch.cat([state_emb, history_emb, p_metrics, v_metrics, s_metrics, x_metrics], dim=-1)
        agent_weights = self.mediator(sim_input)
        
        # 4. Final Consensus
        final_probs = (agent_weights[:, 0:1] * p_probs + 
                       agent_weights[:, 1:2] * v_probs + 
                       agent_weights[:, 2:3] * s_probs + 
                       agent_weights[:, 3:4] * x_probs)
        
        return final_probs, agent_weights

    def forward_latent(self, state_emb, history_emb=None, num_nodes=None, total_nodes=None):
        """
        MCTS Evaluation Path.
        Performs the exact same negotiation but entirely in the latent space 
        using the World Model's transition function.
        """
        if history_emb is None:
            history_emb = torch.zeros(state_emb.size(0), self.history_dim, device=state_emb.device)
        
        specialist_input = torch.cat([state_emb, history_emb], dim=-1)
        
        # 1. Generate Proposals (history-aware)
        p_probs, _ = self.performance_agent(specialist_input)
        v_probs, _ = self.speed_agent(specialist_input)
        s_probs, _ = self.size_agent(specialist_input)
        x_probs, _ = self.security_agent(specialist_input)
        
        # Sample most likely action for each agent to simulate
        p_act = torch.argmax(p_probs, dim=-1)
        v_act = torch.argmax(v_probs, dim=-1)
        s_act = torch.argmax(s_probs, dim=-1)
        x_act = torch.argmax(x_probs, dim=-1)
        
        # 2. Simulation Phase (Using v5 World Model latent transition)
        batch_size = state_emb.size(0)
        action_dim = self.world_model.action_dim
        if num_nodes is None:
            num_nodes = torch.full((batch_size,), 100.0, dtype=torch.float32, device=state_emb.device)
        
        def make_onehot(act):
            real_act = act + self.action_offset
            oh = torch.zeros(batch_size, action_dim, device=state_emb.device)
            oh.scatter_(1, real_act.view(-1, 1), 1.0)
            return oh
        
        _, p_metrics = self.world_model.transition_step(state_emb, make_onehot(p_act), num_nodes=num_nodes, total_nodes=total_nodes)
        _, v_metrics = self.world_model.transition_step(state_emb, make_onehot(v_act), num_nodes=num_nodes, total_nodes=total_nodes)
        _, s_metrics = self.world_model.transition_step(state_emb, make_onehot(s_act), num_nodes=num_nodes, total_nodes=total_nodes)
        _, x_metrics = self.world_model.transition_step(state_emb, make_onehot(x_act), num_nodes=num_nodes, total_nodes=total_nodes)
            
        # 3. Mediation Phase (history-aware)
        sim_input = torch.cat([state_emb, history_emb, p_metrics, v_metrics, s_metrics, x_metrics], dim=-1)
        agent_weights = self.mediator(sim_input)
        
        # 4. Final Consensus
        final_probs = (agent_weights[:, 0:1] * p_probs + 
                       agent_weights[:, 1:2] * v_probs + 
                       agent_weights[:, 2:3] * s_probs + 
                       agent_weights[:, 3:4] * x_probs)
        
        return final_probs, agent_weights

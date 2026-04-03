import numpy as np
from typing import List, Optional
from ..config import POLYBENCH_CATEGORIES

class ContextEncoder:
    def __init__(self):
        self.categories = sorted(POLYBENCH_CATEGORIES)
        self.goals = ["speed", "size"]
        
    def encode(self, category: str, goal: str = "speed") -> np.ndarray:
        cat_vec = np.zeros(len(self.categories), dtype=np.float32)
        normalized_cat = category.lower().strip()
        
        found = False
        for i, cat in enumerate(self.categories):
            if cat in normalized_cat:
                cat_vec[i] = 1.0
                found = True
                break
        
        goal_vec = np.zeros(len(self.goals), dtype=np.float32)
        if goal in self.goals:
            goal_vec[self.goals.index(goal)] = 1.0
        else:
            goal_vec[0] = 1.0
            
        return np.concatenate([cat_vec, goal_vec])

    @property
    def output_dim(self) -> int:
        return len(self.categories) + len(self.goals)

    def get_feature_names(self) -> List[str]:
        names = [f"ctx_cat_{c}" for c in self.categories]
        names += [f"ctx_goal_{g}" for g in self.goals]
        return names

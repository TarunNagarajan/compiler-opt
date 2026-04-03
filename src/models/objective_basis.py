import torch

# Stable index order for multi-task objective prediction.
OBJECTIVE_BASIS_KEYS = [
    "d_runtime_pct",
    "d_energy_pct",
    "d_instr_pct",
    "d_size_pct",
    "d_loads_pct",
    "d_stores_pct",
    "d_allocas_pct",
    "d_branches_pct",
    "d_calls_pct",
    "d_blocks_pct",
]

OBJECTIVE_BASIS_INDEX = {k: i for i, k in enumerate(OBJECTIVE_BASIS_KEYS)}
OBJECTIVE_BASIS_DIM = len(OBJECTIVE_BASIS_KEYS)


def mission_utility_from_objective(mu: torch.Tensor, logvar: torch.Tensor, mission: str, w_size: float, w_speed: float, w_energy: float, uncertainty_weight: float = 0.15):
    """
    Compute mission utility from objective-basis predictions.

    Args:
      mu: [batch, objective_dim] predicted means in percentage deltas.
      logvar: [batch, objective_dim] predicted log-variances.
      mission: "performance" or "embedded".
    """
    if mu.dim() != 2:
        raise ValueError(f"mu must be rank-2 [batch, objective_dim], got {tuple(mu.shape)}")
    if logvar.dim() != 2 or logvar.shape != mu.shape:
        raise ValueError(f"logvar must match mu shape {tuple(mu.shape)}, got {tuple(logvar.shape)}")

    runtime = mu[:, OBJECTIVE_BASIS_INDEX["d_runtime_pct"]]
    energy = mu[:, OBJECTIVE_BASIS_INDEX["d_energy_pct"]]
    instr = mu[:, OBJECTIVE_BASIS_INDEX["d_instr_pct"]]

    loads = mu[:, OBJECTIVE_BASIS_INDEX["d_loads_pct"]]
    stores = mu[:, OBJECTIVE_BASIS_INDEX["d_stores_pct"]]
    allocas = mu[:, OBJECTIVE_BASIS_INDEX["d_allocas_pct"]]
    branches = mu[:, OBJECTIVE_BASIS_INDEX["d_branches_pct"]]
    calls = mu[:, OBJECTIVE_BASIS_INDEX["d_calls_pct"]]
    blocks = mu[:, OBJECTIVE_BASIS_INDEX["d_blocks_pct"]]

    edge_proxy = (
        0.24 * loads
        + 0.14 * stores
        + 0.18 * allocas
        + 0.16 * blocks
        + 0.12 * calls
        + 0.16 * branches
    )

    uncertainty_penalty = uncertainty_weight * torch.sqrt(torch.clamp(torch.exp(logvar), min=1e-8)).mean(dim=-1)

    if mission == "performance":
        utility = runtime - uncertainty_penalty
    else:
        utility = (
            (w_size * instr)
            + (w_speed * runtime)
            + (w_energy * energy)
            + (10.0 * edge_proxy)
            - uncertainty_penalty
        )

    return utility, edge_proxy

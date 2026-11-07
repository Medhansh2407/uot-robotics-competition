from __future__ import annotations

from dataclasses import dataclass

import torch


@dataclass(frozen=True)
class ProductionPolicy:
    initial_fraction_of_median: float = 0.75
    max_initial_kg: float | None = None


@dataclass(frozen=True)
class ProductionRecommendation:
    initial_batch_kg: float
    ingredient_ceiling_kg: float
    reserve_kg: float


def recommend_production(
    quantile_prediction: torch.Tensor,
    policy: ProductionPolicy = ProductionPolicy(),
) -> ProductionRecommendation:
    if quantile_prediction.shape != (3,):
        raise ValueError("quantile_prediction must have shape [3]")
    if not 0 < policy.initial_fraction_of_median <= 1:
        raise ValueError("initial_fraction_of_median must be in (0, 1]")
    if policy.max_initial_kg is not None and policy.max_initial_kg < 0:
        raise ValueError("max_initial_kg cannot be negative")
    p50 = float(quantile_prediction[1].item())
    p90 = float(quantile_prediction[2].item())
    initial = p50 * policy.initial_fraction_of_median
    if policy.max_initial_kg is not None:
        initial = min(initial, policy.max_initial_kg)
    return ProductionRecommendation(
        initial_batch_kg=initial,
        ingredient_ceiling_kg=p90,
        reserve_kg=max(0.0, p90 - initial),
    )

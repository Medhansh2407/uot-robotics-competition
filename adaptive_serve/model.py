from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F


QUANTILES = (0.10, 0.50, 0.90)


@dataclass(frozen=True)
class ModelConfig:
    num_food_items: int
    num_numeric_features: int = 9
    num_meal_periods: int = 3
    num_days: int = 7
    hidden_size: int = 64
    dropout: float = 0.10


class ResidualBlock(nn.Module):
    def __init__(self, hidden_size: int, dropout: float) -> None:
        super().__init__()
        self.layers = nn.Sequential(
            nn.LayerNorm(hidden_size),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.SiLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_size * 2, hidden_size),
        )

    def forward(self, values: torch.Tensor) -> torch.Tensor:
        return values + self.layers(values)


class DemandQuantileModel(nn.Module):
    """Predict ordered P10, P50 and P90 next-day food demand in kilograms."""

    def __init__(self, config: ModelConfig) -> None:
        super().__init__()
        if config.num_food_items < 1:
            raise ValueError("num_food_items must be positive")
        self.config = config
        self.food_embedding = nn.Embedding(config.num_food_items, 8)
        self.meal_embedding = nn.Embedding(config.num_meal_periods, 3)
        self.day_embedding = nn.Embedding(config.num_days, 4)
        input_size = 8 + 3 + 4 + config.num_numeric_features
        self.input_layer = nn.Sequential(
            nn.Linear(input_size, config.hidden_size),
            nn.LayerNorm(config.hidden_size),
            nn.SiLU(),
        )
        self.blocks = nn.Sequential(
            ResidualBlock(config.hidden_size, config.dropout),
            ResidualBlock(config.hidden_size, config.dropout),
        )
        self.head = nn.Linear(config.hidden_size, 3)

    def forward(self, categorical: torch.Tensor, numeric: torch.Tensor) -> torch.Tensor:
        if categorical.ndim != 2 or categorical.shape[1] != 3:
            raise ValueError("categorical input must have shape [batch, 3]")
        if numeric.ndim != 2 or numeric.shape[1] != self.config.num_numeric_features:
            raise ValueError(
                f"numeric input must have shape [batch, {self.config.num_numeric_features}]"
            )
        encoded = torch.cat(
            (
                self.food_embedding(categorical[:, 0]),
                self.meal_embedding(categorical[:, 1]),
                self.day_embedding(categorical[:, 2]),
                numeric,
            ),
            dim=1,
        )
        raw = self.head(self.blocks(self.input_layer(encoded)))
        p10 = F.softplus(raw[:, 0])
        p50 = p10 + F.softplus(raw[:, 1])
        p90 = p50 + F.softplus(raw[:, 2])
        return torch.stack((p10, p50, p90), dim=1)


def pinball_loss(
    predictions: torch.Tensor,
    target: torch.Tensor,
    quantiles: tuple[float, ...] = QUANTILES,
) -> torch.Tensor:
    if predictions.ndim != 2 or predictions.shape[1] != len(quantiles):
        raise ValueError("predictions must have one column per quantile")
    if target.ndim != 1 or target.shape[0] != predictions.shape[0]:
        raise ValueError("target must have shape [batch]")
    levels = predictions.new_tensor(quantiles).view(1, -1)
    error = target.unsqueeze(1) - predictions
    return torch.maximum(levels * error, (levels - 1.0) * error).mean()

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import torch


CATEGORICAL_COLUMNS = ("food_item_id", "meal_period", "day_of_week")
NUMERIC_COLUMNS = (
    "expected_attendance",
    "attendance_7d_ago",
    "served_kg_1d_ago",
    "served_kg_7d_ago",
    "unserved_kg_1d_ago",
    "plate_waste_kg_1d_ago",
    "rolling_mean_demand_28d",
    "rolling_std_demand_28d",
    "is_special_event",
)
TARGET_COLUMN = "next_day_demand_kg"


@dataclass(frozen=True)
class DemandTensors:
    categorical: torch.Tensor
    numeric: torch.Tensor
    target: torch.Tensor


@dataclass(frozen=True)
class FeatureNormalizer:
    mean: torch.Tensor
    scale: torch.Tensor

    @classmethod
    def fit(cls, values: torch.Tensor) -> "FeatureNormalizer":
        if values.ndim != 2 or values.shape[0] == 0:
            raise ValueError("numeric features must be a non-empty 2D tensor")
        mean = values.mean(dim=0)
        scale = values.std(dim=0, unbiased=False).clamp_min(1e-6)
        return cls(mean=mean, scale=scale)

    def transform(self, values: torch.Tensor) -> torch.Tensor:
        return (values - self.mean.to(values.device)) / self.scale.to(values.device)

    def state_dict(self) -> dict[str, torch.Tensor]:
        return {"mean": self.mean, "scale": self.scale}


def chronological_split(
    num_rows: int,
    train_fraction: float = 0.70,
    validation_fraction: float = 0.15,
) -> tuple[range, range, range]:
    if num_rows < 3:
        raise ValueError("at least three chronological rows are required")
    if train_fraction <= 0 or validation_fraction <= 0:
        raise ValueError("split fractions must be positive")
    train_end = int(num_rows * train_fraction)
    validation_end = train_end + int(num_rows * validation_fraction)
    if train_end == 0 or validation_end <= train_end or validation_end >= num_rows:
        raise ValueError("split fractions leave an empty partition")
    return range(0, train_end), range(train_end, validation_end), range(validation_end, num_rows)


def load_csv(path: str | Path) -> DemandTensors:
    required = set(CATEGORICAL_COLUMNS + NUMERIC_COLUMNS + (TARGET_COLUMN,))
    categorical_rows: list[list[int]] = []
    numeric_rows: list[list[float]] = []
    targets: list[float] = []

    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        missing = required - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"CSV is missing columns: {sorted(missing)}")
        for line_number, row in enumerate(reader, start=2):
            try:
                categorical_rows.append([int(row[name]) for name in CATEGORICAL_COLUMNS])
                numeric_rows.append([float(row[name]) for name in NUMERIC_COLUMNS])
                target = float(row[TARGET_COLUMN])
            except (TypeError, ValueError) as error:
                raise ValueError(f"invalid value on CSV line {line_number}") from error
            if target < 0:
                raise ValueError(f"negative target on CSV line {line_number}")
            targets.append(target)

    if not targets:
        raise ValueError("CSV contains no data rows")
    return DemandTensors(
        categorical=torch.tensor(categorical_rows, dtype=torch.long),
        numeric=torch.tensor(numeric_rows, dtype=torch.float32),
        target=torch.tensor(targets, dtype=torch.float32),
    )


def make_synthetic_data(
    num_samples: int = 1_200,
    num_food_items: int = 12,
    seed: int = 7,
) -> DemandTensors:
    if num_samples < 3 or num_food_items < 1:
        raise ValueError("synthetic data needs at least three rows and one food item")

    generator = torch.Generator().manual_seed(seed)
    row = torch.arange(num_samples)
    food = row.remainder(num_food_items)
    meal = torch.div(row, num_food_items, rounding_mode="floor").remainder(3)
    day = torch.div(row, num_food_items * 3, rounding_mode="floor").remainder(7)
    event = (torch.rand(num_samples, generator=generator) < 0.08).float()

    food_popularity = 4.0 + food.float() * 0.7
    meal_multiplier = torch.tensor([0.75, 1.20, 1.00])[meal]
    weekend_multiplier = torch.where(day >= 5, 0.78, 1.0)
    event_multiplier = 1.0 + 0.30 * event
    full_meal_demand = food_popularity * meal_multiplier * weekend_multiplier * event_multiplier
    noise = torch.randn(num_samples, generator=generator) * 0.45
    target = (full_meal_demand + noise).clamp_min(0.0)

    expected_attendance = (target * 10.0 + torch.randn(num_samples, generator=generator) * 4.0).clamp_min(0.0)
    attendance_7d_ago = (expected_attendance + torch.randn(num_samples, generator=generator) * 7.0).clamp_min(0.0)
    served_1d = (target + torch.randn(num_samples, generator=generator) * 0.9).clamp_min(0.0)
    served_7d = (target + torch.randn(num_samples, generator=generator) * 0.7).clamp_min(0.0)
    unserved_1d = torch.rand(num_samples, generator=generator) * 1.2
    plate_waste_1d = served_1d * (0.04 + torch.rand(num_samples, generator=generator) * 0.14)
    rolling_mean = (target + torch.randn(num_samples, generator=generator) * 0.8).clamp_min(0.0)
    rolling_std = (0.5 + torch.rand(num_samples, generator=generator) * 1.5)

    categorical = torch.stack((food, meal, day), dim=1).long()
    numeric = torch.stack(
        (
            expected_attendance,
            attendance_7d_ago,
            served_1d,
            served_7d,
            unserved_1d,
            plate_waste_1d,
            rolling_mean,
            rolling_std,
            event,
        ),
        dim=1,
    ).float()
    return DemandTensors(categorical=categorical, numeric=numeric, target=target.float())

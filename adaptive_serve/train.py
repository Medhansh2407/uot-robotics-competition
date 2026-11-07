from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

from .data import (
    NUMERIC_COLUMNS,
    FeatureNormalizer,
    chronological_split,
    load_csv,
    make_synthetic_data,
)
from .model import DemandQuantileModel, ModelConfig, pinball_loss


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the AdaptiveServe demand forecaster")
    parser.add_argument("--csv", type=Path, help="chronologically sorted training CSV")
    parser.add_argument("--output", type=Path, default=Path("artifacts/demand_model.pt"))
    parser.add_argument("--epochs", type=int, default=60)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=3e-3)
    parser.add_argument("--synthetic-samples", type=int, default=1_200)
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


def evaluate(
    model: nn.Module,
    categorical: torch.Tensor,
    numeric: torch.Tensor,
    target: torch.Tensor,
) -> dict[str, float]:
    model.eval()
    with torch.no_grad():
        predictions = model(categorical, numeric)
        loss = pinball_loss(predictions, target)
        median_mae = (predictions[:, 1] - target).abs().mean()
        interval_coverage = (
            ((target >= predictions[:, 0]) & (target <= predictions[:, 2])).float().mean()
        )
    return {
        "pinball_loss": float(loss.item()),
        "median_mae_kg": float(median_mae.item()),
        "p10_p90_coverage": float(interval_coverage.item()),
    }


def main() -> None:
    args = parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        raise ValueError("epochs and batch size must be positive")
    torch.manual_seed(args.seed)

    data = load_csv(args.csv) if args.csv else make_synthetic_data(
        num_samples=args.synthetic_samples,
        seed=args.seed,
    )
    train_rows, validation_rows, test_rows = chronological_split(len(data.target))
    train_index = torch.tensor(list(train_rows))
    validation_index = torch.tensor(list(validation_rows))
    test_index = torch.tensor(list(test_rows))

    normalizer = FeatureNormalizer.fit(data.numeric[train_index])
    numeric = normalizer.transform(data.numeric)
    config = ModelConfig(
        num_food_items=int(data.categorical[:, 0].max().item()) + 1,
        num_numeric_features=data.numeric.shape[1],
    )
    model = DemandQuantileModel(config)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    generator = torch.Generator().manual_seed(args.seed)
    loader = DataLoader(
        TensorDataset(
            data.categorical[train_index],
            numeric[train_index],
            data.target[train_index],
        ),
        batch_size=args.batch_size,
        shuffle=True,
        generator=generator,
    )

    best_state: dict[str, torch.Tensor] | None = None
    best_validation = float("inf")
    first_epoch_loss = 0.0
    for epoch in range(args.epochs):
        model.train()
        running_loss = 0.0
        row_count = 0
        for categorical_batch, numeric_batch, target_batch in loader:
            optimizer.zero_grad(set_to_none=True)
            predictions = model(categorical_batch, numeric_batch)
            loss = pinball_loss(predictions, target_batch)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), max_norm=5.0)
            optimizer.step()
            running_loss += float(loss.item()) * len(target_batch)
            row_count += len(target_batch)
        epoch_loss = running_loss / row_count
        if epoch == 0:
            first_epoch_loss = epoch_loss

        validation = evaluate(
            model,
            data.categorical[validation_index],
            numeric[validation_index],
            data.target[validation_index],
        )
        if validation["pinball_loss"] < best_validation:
            best_validation = validation["pinball_loss"]
            best_state = {name: value.detach().clone() for name, value in model.state_dict().items()}

    if best_state is None:
        raise RuntimeError("training did not produce a checkpoint")
    model.load_state_dict(best_state)
    test_metrics = evaluate(
        model,
        data.categorical[test_index],
        numeric[test_index],
        data.target[test_index],
    )
    baseline_mae = (
        data.numeric[test_index, 6] - data.target[test_index]
    ).abs().mean().item()
    test_metrics["rolling_mean_baseline_mae_kg"] = float(baseline_mae)
    test_metrics["first_epoch_train_loss"] = first_epoch_loss
    test_metrics["best_validation_loss"] = best_validation

    args.output.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "schema_version": 1,
            "model_config": asdict(config),
            "model_state": model.state_dict(),
            "normalizer": normalizer.state_dict(),
            "numeric_columns": NUMERIC_COLUMNS,
            "metrics": test_metrics,
        },
        args.output,
    )
    print(json.dumps({"checkpoint": str(args.output), "metrics": test_metrics}, indent=2))


if __name__ == "__main__":
    main()

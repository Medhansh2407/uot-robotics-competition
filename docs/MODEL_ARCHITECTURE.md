# AdaptiveServe demand model

## Prediction contract

Each row represents one planned menu item for tomorrow's breakfast, lunch, or dinner. The target is `next_day_demand_kg`: kilograms expected to be served during that service.

The model predicts three ordered values:

- P10: low-demand scenario
- P50: median expected demand and the basis for initial cooking
- P90: high-demand scenario used as the ingredient-preparation ceiling

The production policy cooks a configurable fraction of P50 initially and keeps enough prepared ingredients to reach P90 in later batches. The model advises staff; it does not control cooking equipment.

## Inputs

Categorical embeddings:

- `food_item_id`
- `meal_period`: 0 breakfast, 1 lunch, 2 dinner
- `day_of_week`: 0–6 under one documented convention

Normalized numeric features:

- aggregate `expected_attendance`
- aggregate `attendance_7d_ago`
- `served_kg_1d_ago`
- `served_kg_7d_ago`
- `unserved_kg_1d_ago`
- `plate_waste_kg_1d_ago`
- `rolling_mean_demand_28d`
- `rolling_std_demand_28d`
- `is_special_event`

No student identifiers, faces, payment information, or individual meal histories are model inputs.

## Architecture

```text
food embedding (8) ─┐
meal embedding (3) ─┼─ concat ─ linear(64) ─ two residual MLP blocks ─ head(3)
day embedding (4) ──┤
numeric features (9)┘

head outputs ─ softplus cumulative deltas ─ ordered P10 ≤ P50 ≤ P90
```

The small mixed-input MLP is preferred over an LSTM or Transformer initially because historical context is represented through explicit lag and rolling features, while the expected competition dataset is small. A sequence model should be considered only after repeated evidence that temporal information lost by this representation limits accuracy.

Training uses pinball loss for P10/P50/P90, AdamW, gradient clipping, chronological train/validation/test splits, and selection by validation pinball loss.

## CSV schema

The training CLI accepts a chronologically sorted CSV with all input columns above plus `next_day_demand_kg`. Category columns must currently be integer encoded. Rows affected by stockouts are censored demand observations and should be excluded or corrected until unmet demand can be estimated reliably.

## Run

Synthetic smoke test:

```bash
python -m adaptive_serve.train --epochs 60 --output artifacts/demand_model.pt
```

Real data:

```bash
python -m adaptive_serve.train --csv path/to/chronological_rows.csv
```

Do not deploy a checkpoint until it beats the rolling-mean baseline on future chronological data and its P10–P90 interval coverage is calibrated on real cafeteria observations.

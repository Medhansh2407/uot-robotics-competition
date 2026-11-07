# AdaptiveServe data collection protocol

## Recommended sensor stack

Use aggregate attendance data plus a shared weighing station as the production MVP. Do not put a scale under every hot serving pan and do not make cameras the primary measurement.

1. Reuse an aggregate entrance count for each meal period. Student identities are neither stored nor supplied to the model.
2. Give each food pan a washable QR or NFC tag containing only a pan identifier.
3. Weigh the tagged pan at a stainless-steel station when it leaves the kitchen and when it returns. The pan's stored tare weight converts gross weight to food weight.
4. Record transfers, spills, donations, and stockouts through four large staff buttons in the logging interface.
5. Add a load cell under the disposal bin only if plate-waste mass is needed.
6. Treat an overhead disposal-zone camera as an optional second-phase classifier. It may classify broad food categories on-device, but it must not capture faces, identify diners, or retain video.

This configuration measures mass accurately with one serviceable scale and identifies the food through the pan tag. Camera-only estimates are vulnerable to occlusion, lighting, mixed foods, and container geometry. Permanent under-pan load cells are exposed to heat, steam, cleaning, drift, and frequent recalibration.

## Measurement workflow

At a fixed cutoff each evening, create tomorrow's feature rows from information already known at that time. Never calculate a training feature using future service data.

For every date, meal period, and menu item, record:

| Field | Source | Unit or values |
| --- | --- | --- |
| `food_item_id` | stable menu catalogue | integer category |
| `meal_period` | schedule | 0 breakfast, 1 lunch, 2 dinner |
| `day_of_week` | calendar | 0–6 under one documented convention |
| `expected_attendance` | aggregate forecast | people |
| `attendance_7d_ago` | aggregate entrance count | people |
| `produced_kg` | tagged pan outgoing weights | kg |
| `served_kg` | produced minus returns and recorded transfers | kg |
| `unserved_kg` | tagged pan return weights | kg |
| `plate_waste_kg` | waste-station scale, if installed | kg |
| `stockout_minutes` | staff event log | minutes |
| `is_special_event` | calendar | 0 or 1 |

The training pipeline derives one-day and seven-day lags plus 28-day rolling statistics from this event table.

## Target and data-quality rules

`next_day_demand_kg` means the amount diners would have taken if the item remained available. On a day without a stockout, use `served_kg` as the target. A stockout censors true demand: initially exclude that row from training, then add an explicit unmet-demand estimate only after it has been validated.

Plate waste is a separate outcome, not something to subtract from demand. High servings plus high plate waste can mean poor acceptance or oversized portions; lowering total production alone would hide that problem. Use plate waste later for portion-size and menu-quality recommendations.

Validate each shift by checking the mass balance:

```text
produced = served + unserved + transfers + spills ± measurement error
```

Flag rows outside a documented tolerance for review. Calibrate the shared scale with a known mass at the start of each day and log the result.

## Pilot cadence

- Week 0: catalogue pans/menu items, record tare weights, and train staff on the four exception buttons.
- Weeks 1–2: measure only; do not let the model change production.
- Weeks 3–6: continue measuring, establish the rolling baseline, and inspect missing or inconsistent rows.
- After enough repeated menu observations: run the model in shadow mode and compare it with the rolling baseline.
- Deploy recommendations only after future chronological tests beat the baseline and staff can override every recommendation.

Two weeks is enough for a demonstration, not a trustworthy seasonal forecasting model. Continue collecting through schedule changes, holidays, weather patterns, and menu rotations.

## Privacy and operational boundaries

- Store counts, not student identities, card numbers, faces, or payment records.
- Aim any optional camera only at the disposal surface, process locally, and discard frames after classification.
- Keep sensors outside food-contact surfaces or use housings and cleaning procedures approved by food-service staff.
- The model recommends quantities; a trained staff member remains responsible for cooking, holding temperatures, allergen controls, and final service decisions.

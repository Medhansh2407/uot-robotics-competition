import tempfile
import unittest
from pathlib import Path

import torch

from adaptive_serve.data import FeatureNormalizer, chronological_split, make_synthetic_data
from adaptive_serve.model import DemandQuantileModel, ModelConfig, pinball_loss
from adaptive_serve.policy import ProductionPolicy, recommend_production


class DemandModelTest(unittest.TestCase):
    def setUp(self) -> None:
        torch.manual_seed(7)
        self.config = ModelConfig(num_food_items=6, num_numeric_features=9)
        self.model = DemandQuantileModel(self.config)

    def test_outputs_are_nonnegative_and_ordered(self) -> None:
        categorical = torch.tensor([[0, 0, 0], [5, 2, 6]], dtype=torch.long)
        numeric = torch.randn(2, 9)

        predictions = self.model(categorical, numeric)

        self.assertEqual(tuple(predictions.shape), (2, 3))
        self.assertTrue(torch.all(predictions >= 0))
        self.assertTrue(torch.all(predictions[:, 0] <= predictions[:, 1]))
        self.assertTrue(torch.all(predictions[:, 1] <= predictions[:, 2]))

    def test_pinball_loss_prefers_better_predictions(self) -> None:
        target = torch.tensor([10.0, 20.0])
        good = torch.tensor([[8.0, 10.0, 12.0], [18.0, 20.0, 22.0]])
        bad = torch.tensor([[1.0, 2.0, 3.0], [40.0, 45.0, 50.0]])

        self.assertLess(pinball_loss(good, target), pinball_loss(bad, target))

    def test_checkpoint_round_trip_preserves_predictions(self) -> None:
        categorical = torch.tensor([[1, 1, 3]], dtype=torch.long)
        numeric = torch.randn(1, 9)
        self.model.eval()
        expected = self.model(categorical, numeric).detach()

        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.pt"
            torch.save(self.model.state_dict(), path)
            restored = DemandQuantileModel(self.config)
            restored.load_state_dict(torch.load(path, weights_only=True))
            restored.eval()

        actual = restored(categorical, numeric).detach()
        torch.testing.assert_close(actual, expected)


class DataAndPolicyTest(unittest.TestCase):
    def test_normalizer_uses_training_statistics(self) -> None:
        values = torch.tensor([[1.0, 10.0], [3.0, 14.0], [5.0, 18.0]])
        normalizer = FeatureNormalizer.fit(values)
        normalized = normalizer.transform(values)

        torch.testing.assert_close(normalized.mean(dim=0), torch.zeros(2), atol=1e-6, rtol=0)
        torch.testing.assert_close(normalized.std(dim=0, unbiased=False), torch.ones(2), atol=1e-6, rtol=0)

    def test_chronological_split_does_not_mix_future_rows(self) -> None:
        train, validation, test = chronological_split(100)

        self.assertEqual((len(train), len(validation), len(test)), (70, 15, 15))
        self.assertLess(max(train), min(validation))
        self.assertLess(max(validation), min(test))

    def test_synthetic_data_matches_schema(self) -> None:
        data = make_synthetic_data(num_samples=64, num_food_items=5, seed=4)

        self.assertEqual(tuple(data.categorical.shape), (64, 3))
        self.assertEqual(tuple(data.numeric.shape), (64, 9))
        self.assertEqual(tuple(data.target.shape), (64,))
        self.assertTrue(torch.all(data.target >= 0))

    def test_production_policy_stages_median_and_reserves_to_upper_quantile(self) -> None:
        prediction = torch.tensor([8.0, 10.0, 14.0])
        recommendation = recommend_production(
            prediction,
            ProductionPolicy(initial_fraction_of_median=0.75, max_initial_kg=8.0),
        )

        self.assertEqual(recommendation.initial_batch_kg, 7.5)
        self.assertEqual(recommendation.ingredient_ceiling_kg, 14.0)
        self.assertEqual(recommendation.reserve_kg, 6.5)


if __name__ == "__main__":
    unittest.main()

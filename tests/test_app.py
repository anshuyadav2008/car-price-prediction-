import unittest

from app import app


class AppRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage_renders(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Calculate your car's value", response.data)

    def test_summary_returns_model_metrics(self):
        response = self.client.get("/api/summary")
        summary = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(summary["total_cars"], 301)
        self.assertEqual(summary["features"], 7)
        self.assertIn("r2", summary)
        self.assertIn("mae", summary)

    def test_valid_prediction_returns_price(self):
        response = self.client.post(
            "/predict",
            json={
                "year": "2017",
                "present_price": "8.5",
                "kms_driven": "25000",
                "fuel_type": "Petrol",
                "seller_type": "Dealer",
                "transmission": "Manual",
                "owner": "0",
            },
        )
        prediction = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(prediction["predicted_price"], 0)
        self.assertIn("Lakh", prediction["formatted_price"])

    def test_invalid_fuel_type_is_rejected(self):
        response = self.client.post(
            "/predict",
            json={
                "year": "2017",
                "present_price": "8.5",
                "kms_driven": "25000",
                "fuel_type": "Electric",
                "seller_type": "Dealer",
                "transmission": "Manual",
                "owner": "0",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest

from src.scoring import ai_brief, explain_risk, next_best_action, score_customer
from src.workflow import read_events, record_event


ROOT = Path(__file__).resolve().parents[1]


class DecisionTests(unittest.TestCase):
    def setUp(self):
        self.customer = pd.read_csv(ROOT / "data/customers.csv").iloc[0]
        self.history = pd.read_csv(ROOT / "data/interactions.csv", parse_dates=["interaction_date"])
        self.history = self.history[self.history.customer_id == "C1001"].copy()

    def test_closed_claim_does_not_trigger_claim_action(self):
        self.history["status"] = "Closed"
        self.assertNotEqual(next_best_action(self.customer, self.history, 60)["action"], "Fast-track claim review")

    def test_unresolved_claim_survives_newer_unrelated_touchpoint(self):
        self.history.loc[self.history.issue_type == "Service Request", "interaction_date"] = pd.Timestamp("2026-10-01")
        for history in (self.history, self.history.iloc[::-1]):
            self.assertEqual(next_best_action(self.customer, history, 95)["action"], "Fast-track claim review")

    def test_open_case_blocks_cross_sell_even_at_low_score(self):
        customer = self.customer.copy()
        customer["product_count"] = 1
        self.history["issue_type"] = "General"
        self.assertEqual(next_best_action(customer, self.history, 10)["action"], "Resolve open service case")

    def test_missing_history_does_not_trigger_cross_sell(self):
        customer = self.customer.copy()
        customer["product_count"] = 1
        self.assertEqual(next_best_action(customer, self.history.iloc[:0], 10)["action"], "Maintain and nurture")

    def test_explanation_reconciles_with_bounded_score(self):
        for history in (self.history, self.history.iloc[:0], pd.concat([self.history] * 20)):
            expected = max(0, min(100, int(sum(row["impact"] for row in explain_risk(self.customer, history)))))
            self.assertEqual(score_customer(self.customer, history), expected)

    def test_brief_uses_latest_date_not_row_order(self):
        action = next_best_action(self.customer, self.history, 70)
        self.assertEqual(ai_brief(self.customer, self.history, action), ai_brief(self.customer, self.history.iloc[::-1], action))

    def test_resolution_scenario_preserves_original(self):
        scenario = self.history.copy()
        scenario["status"] = "Closed"
        self.assertLess(score_customer(self.customer, scenario), score_customer(self.customer, self.history))
        self.assertEqual(int((self.history.status == "Open").sum()), 1)


class WorkflowTests(unittest.TestCase):
    def test_persistence_transitions_duplicate_and_notes(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "events.db"
            action = {"action": "Claim review", "owner": "Claims"}
            def save(status, notes=""):
                record_event("C1001", action, 75, status, notes, ["I5001"], path)
            with self.assertRaises(ValueError):
                save("Resolved", "Case verified closed")
            save("Accepted")
            with self.assertRaises(ValueError):
                save("Accepted")
            with self.assertRaises(ValueError):
                save("Resolved")
            save("Resolved", "Case verified closed")
            events = read_events(path)
            self.assertEqual([item["status"] for item in events], ["Resolved", "Accepted"])
            self.assertEqual(events[0]["evidence_ids"], '["I5001"]')


class AppTests(unittest.TestCase):
    def test_all_customers_empty_filters_and_simulation(self):
        with patch("src.workflow.read_events", return_value=[]):
            app = AppTest.from_file(str(ROOT / "app.py")).run()
            self.assertFalse(app.exception)
            self.assertEqual(len(app.tabs), 9)
            for customer_id in app.radio[0].options:
                # Radio options expose formatted labels; use the stored ID.
                app.radio[0].set_value(customer_id[-6:-1]).run()
                self.assertFalse(app.exception)
            app.radio[0].set_value("C1001").run()
            app.multiselect[2].set_value(["I5001"]).run()
            self.assertFalse(app.exception)
            app.multiselect[0].set_value([]).run()
            self.assertFalse(app.exception)
            self.assertTrue(any("No matching" in item.value for item in app.warning))
            self.assertTrue(any(item.value == "Submission Evidence" for item in app.subheader))

    def test_decision_round_trip_in_ui(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "events.db"
            original_record = record_event
            with patch("src.workflow.read_events", side_effect=lambda: read_events(path)), patch(
                "src.workflow.record_event", side_effect=lambda *args: original_record(*args, path=path)
            ):
                app = AppTest.from_file(str(ROOT / "app.py")).run()
                app.button[0].click().run()
                self.assertFalse(app.exception)
                self.assertEqual(read_events(path)[0]["status"], "Accepted")
                app.selectbox[0].set_value("Resolved")
                app.text_area[0].set_value("Synthetic test: case owner confirmed resolution")
                app.button[0].click().run()
                self.assertFalse(app.exception)
                self.assertEqual(read_events(path)[0]["status"], "Resolved")
                self.assertEqual(len(read_events(path)), 2)


if __name__ == "__main__":
    unittest.main()

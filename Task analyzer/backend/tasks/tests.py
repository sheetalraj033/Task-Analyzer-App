from django.test import TestCase
from datetime import date, timedelta
from .scoring import calculate_task_score

class ScoringTests(TestCase):

    def test_overdue_task_has_high_urgency(self):
        """Urgency should be max (10) for overdue tasks."""
        task = {
            "id": 1,
            "title": "Overdue Task",
            "due_date": date.today() - timedelta(days=2),
            "estimated_hours": 2,
            "importance": 5,
            "dependencies": []
        }
        score, explanation = calculate_task_score(task, [task])
        self.assertEqual(explanation["urgency_score"], 10)

    def test_importance_affects_score(self):
        """Tasks with higher importance should have higher score."""
        today = date.today()
        low_imp = {
            "id": 1,
            "title": "Low Importance",
            "due_date": today,
            "estimated_hours": 3,
            "importance": 2,
            "dependencies": []
        }
        high_imp = {
            "id": 2,
            "title": "High Importance",
            "due_date": today,
            "estimated_hours": 3,
            "importance": 9,
            "dependencies": []
        }
        score_low, _ = calculate_task_score(low_imp, [low_imp, high_imp])
        score_high, _ = calculate_task_score(high_imp, [low_imp, high_imp])

        self.assertTrue(score_high > score_low)

    def test_effort_score_favors_smaller_tasks(self):
        """Small effort tasks should get higher effort score."""
        today = date.today()
        long_task = {
            "id": 1,
            "title": "Long Task",
            "due_date": today,
            "estimated_hours": 10,
            "importance": 5,
            "dependencies": []
        }
        short_task = {
            "id": 2,
            "title": "Short Task",
            "due_date": today,
            "estimated_hours": 1,
            "importance": 5,
            "dependencies": []
        }

        score_long, exp_long = calculate_task_score(long_task, [long_task, short_task])
        score_short, exp_short = calculate_task_score(short_task, [long_task, short_task])

        self.assertTrue(exp_short["effort_score"] > exp_long["effort_score"])

import unittest
from activities import get_activity_for_date, get_milestones, get_random_activity, ACTIVITIES_DB

class TestActivities(unittest.TestCase):
    def test_get_activity_defaults(self):
        # Test default age group (3)
        act = get_activity_for_date(1, "3")
        self.assertIsNotNone(act)
        self.assertIn("title", act)

    def test_get_activity_age_groups(self):
        act2 = get_activity_for_date(1, "2")
        act5 = get_activity_for_date(1, "5")

        # Ensure we get different activities (conceptually, though indices might align)
        # Checking if they exist in the DB for that age
        self.assertIn(act2, ACTIVITIES_DB["2"])
        self.assertIn(act5, ACTIVITIES_DB["5"])

    def test_milestones(self):
        m2 = get_milestones("2")
        self.assertTrue(len(m2) > 0)
        m_invalid = get_milestones("99")
        self.assertEqual(len(m_invalid), 0)

    def test_random_activity(self):
        act = get_random_activity("3")
        self.assertIsNotNone(act)

        # Test exclusion
        exclude = [act["title"]]
        act_new = get_random_activity("3", exclude_titles=exclude)
        self.assertNotEqual(act_new["title"], act["title"])

if __name__ == '__main__':
    unittest.main()

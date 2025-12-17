import unittest
import db
import os
import json

class TestDB(unittest.TestCase):
    def setUp(self):
        # Use a temporary database for testing
        self.original_db_name = db.DB_NAME
        db.DB_NAME = "test_kids_activity.db"
        db.init_db()

    def tearDown(self):
        # Clean up
        if os.path.exists(db.DB_NAME):
            os.remove(db.DB_NAME)
        db.DB_NAME = self.original_db_name

    def test_user_registration_login(self):
        self.assertTrue(db.register_user("testuser", "password"))
        self.assertTrue(db.login_user("testuser", "password"))
        self.assertFalse(db.login_user("testuser", "wrongpassword"))
        self.assertFalse(db.register_user("testuser", "password")) # Duplicate

    def test_completion_toggle(self):
        db.register_user("user1", "pass")
        self.assertTrue(db.toggle_completion("user1", "2023-10-01"))
        self.assertIn("2023-10-01", db.get_user_completions("user1"))
        self.assertFalse(db.toggle_completion("user1", "2023-10-01"))
        self.assertNotIn("2023-10-01", db.get_user_completions("user1"))

    def test_activity_override(self):
        db.register_user("user1", "pass")
        activity = {"title": "Test Activity", "description": "Desc"}
        db.save_activity_override("user1", "2023-10-01", activity)

        retrieved = db.get_activity_override("user1", "2023-10-01")
        self.assertEqual(retrieved["title"], "Test Activity")

        self.assertIsNone(db.get_activity_override("user1", "2023-10-02"))

if __name__ == '__main__':
    unittest.main()

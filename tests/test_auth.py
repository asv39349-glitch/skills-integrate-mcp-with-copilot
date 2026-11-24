import os
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from src.app import SESSION_COOKIE, app, sessions


class TeacherAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.environment = patch.dict(
            os.environ,
            {
                "TEACHER_USERNAME": "teacher",
                "TEACHER_PASSWORD": "safe-test-password",
            },
        )
        self.environment.start()
        sessions.clear()
        self.client = TestClient(app)

    def tearDown(self):
        self.client.close()
        sessions.clear()
        self.environment.stop()

    def login(self):
        return self.client.post(
            "/auth/login",
            json={"username": "teacher", "password": "safe-test-password"},
        )

    def test_public_can_view_activities_but_cannot_change_registrations(self):
        self.assertEqual(self.client.get("/activities").status_code, 200)

        signup_response = self.client.post(
            "/activities/Chess Club/signup",
            params={"email": "new-student@mergington.edu"},
        )
        unregister_response = self.client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "michael@mergington.edu"},
        )

        self.assertEqual(signup_response.status_code, 401)
        self.assertEqual(unregister_response.status_code, 401)

    def test_teacher_can_manage_registrations_and_logout_revokes_access(self):
        login_response = self.login()
        self.assertEqual(login_response.status_code, 200)
        self.assertIn(SESSION_COOKIE, self.client.cookies)

        signup_response = self.client.post(
            "/activities/Chess Club/signup",
            params={"email": "new-student@mergington.edu"},
        )
        self.assertEqual(signup_response.status_code, 200)

        logout_response = self.client.post("/auth/logout")
        self.assertEqual(logout_response.status_code, 200)

        unregister_response = self.client.delete(
            "/activities/Chess Club/unregister",
            params={"email": "new-student@mergington.edu"},
        )
        self.assertEqual(unregister_response.status_code, 401)

    def test_invalid_credentials_do_not_create_a_session(self):
        response = self.client.post(
            "/auth/login",
            json={"username": "teacher", "password": "wrong-password"},
        )

        self.assertEqual(response.status_code, 401)
        self.assertNotIn(SESSION_COOKIE, self.client.cookies)


if __name__ == "__main__":
    unittest.main()

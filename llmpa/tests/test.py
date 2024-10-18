import unittest
from app import app  # Assuming your Flask app is in app.py


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the test client
        self.app = app.test_client()
        self.app.testing = True

    def test_hello(self):
        # Test the /api/hello route
        response = self.app.get("/api/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, World!"})

    def test_greet_default(self):
        # Test the /api/greet route with default name
        response = self.app.post("/api/greet", json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, Guest!"})

    def test_greet_with_name(self):
        # Test the /api/greet route with a name
        response = self.app.post("/api/greet", json={"name": "Alice"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, Alice!"})

    def test_greet_with_empty_name(self):
        # Test the /api/greet route with an empty name
        response = self.app.post("/api/greet", json={"name": ""})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "Hello, !"})


if __name__ == "__main__":
    unittest.main()

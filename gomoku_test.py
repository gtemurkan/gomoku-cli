import unittest
from unittest.mock import patch, Mock
import requests
from gomoku import GomokuClient


class TestGomokuClient(unittest.TestCase):

    def setUp(self):
        self.client = GomokuClient()
        self.client.SERVER_URL = "http://testserver"

    @patch('requests.post')
    def test_register_success(self, mock_post):
        mock_post.return_value.json.return_value = \
                {"success": True, "message": "User registered successfully."}
        with patch('builtins.input', side_effect=["testuser", "testpass"]):
            self.client.register()
        mock_post.assert_called_with(
            "http://testserver/register",
            json={"username": "testuser", "password": "testpass"}
        )

    @patch('requests.post')
    def test_login_success(self, mock_post):
        mock_post.return_value.json.return_value = \
                {"success": True, "message": "Login successful."}
        with patch('builtins.input', side_effect=["testuser", "testpass"]):
            self.client.login()
        self.assertEqual(self.client.username, "testuser")
        mock_post.assert_called_with(
            "http://testserver/login",
            json={"username": "testuser", "password": "testpass"}
        )

    @patch('requests.post')
    def test_create_game_success(self, mock_post):
        mock_post.return_value.json.return_value = \
            {"success": True, "game_id": 1}
        self.client.username = "testuser"
        self.client.create_game()
        mock_post.assert_called_with(
            "http://testserver/create_game",
            json={"username": "testuser"}
        )


if __name__ == '__main__':
    unittest.main()

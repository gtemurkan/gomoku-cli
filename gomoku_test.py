import unittest
from unittest.mock import patch, Mock
import requests
from gomoku import GomokuClient

class TestGomokuClient(unittest.TestCase):
    """Unit tests for the GomokuClient class."""

    def setUp(self):
        """Initialize a GomokuClient instance and set a test server URL."""
        self.client = GomokuClient()
        self.client.SERVER_URL = "http://testserver"

    @patch('requests.post')
    def test_register_success(self, mock_post):
        """Test successful user registration."""
        mock_post.return_value.json.return_value = {"success": True, "message": "User registered successfully."}
        with patch('builtins.input', side_effect=["testuser", "testpass"]):
            self.client.register()
        mock_post.assert_called_with(
            "http://testserver/register",
            json={"username": "testuser", "password": "testpass"}
        )

    @patch('requests.post')
    def test_register_fail(self, mock_post):
        """Test failed user registration due to existing user."""
        mock_post.return_value.json.return_value = {"success": False, "message": "User already exists."}
        with patch('builtins.input', side_effect=["testuser", "testpass"]):
            self.client.register()
        mock_post.assert_called_with(
            "http://testserver/register",
            json={"username": "testuser", "password": "testpass"}
        )

    @patch('requests.post')
    def test_login_success(self, mock_post):
        """Test successful user login."""
        mock_post.return_value.json.return_value = {"success": True, "message": "Login successful."}
        with patch('builtins.input', side_effect=["testuser", "testpass"]):
            self.client.login()
        self.assertEqual(self.client.username, "testuser")
        mock_post.assert_called_with(
            "http://testserver/login",
            json={"username": "testuser", "password": "testpass"}
        )

    @patch('requests.post')
    def test_login_fail(self, mock_post):
        """Test failed user login due to incorrect credentials."""
        mock_post.return_value.json.return_value = {"success": False, "message": "Invalid username or password."}
        with patch('builtins.input', side_effect=["wronguser", "wrongpass"]):
            self.client.login()
        self.assertIsNone(self.client.username)
        mock_post.assert_called_with(
            "http://testserver/login",
            json={"username": "wronguser", "password": "wrongpass"}
        )

    @patch('requests.post')
    def test_create_game_success(self, mock_post):
        """Test successful game creation."""
        mock_post.return_value.json.return_value = {"success": True, "game_id": 1}
        self.client.username = "testuser"
        self.client.create_game()
        mock_post.assert_called_with(
            "http://testserver/create_game",
            json={"username": "testuser"}
        )

    @patch('requests.post')
    def test_get_ids_all_games_success(self, mock_post):
        """Test successful retrieval of all game IDs."""
        mock_post.return_value.json.return_value = {"success": True, "games": [1, 2, 3]}
        self.client.username = "testuser"
        self.client.get_ids_all_games()
        mock_post.assert_called_with(
            "http://testserver/get_ids_all_games",
            json={"username": "testuser"}
        )

    @patch('requests.post')
    def test_get_ids_all_games_fail(self, mock_post):
        """Test failed retrieval of game IDs due to invalid username."""
        mock_post.return_value.json.return_value = {"success": False, "message": "Invalid username."}
        self.client.username = "unknownuser"
        self.client.get_ids_all_games()
        mock_post.assert_called_with(
            "http://testserver/get_ids_all_games",
            json={"username": "unknownuser"}
        )

if __name__ == '__main__':
    unittest.main()

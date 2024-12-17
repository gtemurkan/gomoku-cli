import unittest
from unittest.mock import patch, MagicMock
from gomoku import GomokuClient


class TestGomokuClient(unittest.TestCase):

    def setUp(self):
        self.client = GomokuClient()
        self.client.SERVER_URL = "https://localhost:8443"

    @patch('gomoku.requests.post')
    def test_register_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "message": "User registered successfully."
        }
        with patch('builtins.input', side_effect=['testuser', 'testpass']):
            self.client.register()
        mock_post.assert_called_once_with(
            f"{self.client.SERVER_URL}/register",
            json={"username": "testuser", "password": "testpass"},
            verify=False
        )

    @patch('gomoku.requests.post')
    def test_login_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "message": "Login successful."}
        with patch('builtins.input', side_effect=['testuser', 'testpass']):
            self.client.login()
        self.assertEqual(self.client.username, 'testuser')

    @patch('gomoku.requests.post')
    def test_create_game_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "game_id": 1}
        self.client.username = "testuser"
        self.client.create_game()
        mock_post.assert_called_once_with(
            f"{self.client.SERVER_URL}/create_game",
            json={"username": "testuser"},
            verify=False
        )

    @patch('gomoku.requests.post')
    def test_view_board_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "board": [["~"] * 19 for _ in range(19)]
        }
        self.client.username = "testuser"
        self.client.game_id = 1
        result = self.client.view_board()
        self.assertEqual(result, "board_is_shown")


if __name__ == '__main__':
    unittest.main()

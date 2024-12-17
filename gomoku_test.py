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

    @patch('gomoku.requests.post')
    def test_get_server_success_server(self, mock_post):
        with patch('builtins.input', side_effect=["server"]):
            self.client.get_server()
        self.assertEqual(self.client.SERVER_URL, "https://109.196.98.96:8443")
        
    @patch('gomoku.requests.post')
    def test_get_server_success_local(self, mock_post):
        with patch('builtins.input', side_effect=["local"]):
            self.client.get_server()
        self.assertEqual(self.client.SERVER_URL, "https://localhost:8443")

    @patch('gomoku.requests.post')
    def test_get_server_success_anyip(self, mock_post):
        with patch('builtins.input', side_effect=["196.128.64.32"]):
            self.client.get_server()
        self.assertEqual(self.client.SERVER_URL, "https://196.128.64.32:8443")


if __name__ == '__main__':
    unittest.main()

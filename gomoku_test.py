import unittest
from unittest.mock import patch, MagicMock
from gomoku import GomokuClient
import io
import sys


class TestGomokuClient(unittest.TestCase):

    def setUp(self):
        self.client = GomokuClient()
        self.client._username = "user1"
        self.client._server_url = "http://localhost:8443"
        self.board = [
            ["●", "~", "~", "~", "~", "~", "~", "~", "~", "~",
                "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~",
             "~", "~", "~", "~", "~", "~", "~", "~", "~"],
        ]

    @patch('gomoku.requests.post')
    def test_login_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "message": "Login successful."}
        with patch('builtins.input', side_effect=['testuser', 'testpass']):
            self.client.login()
        self.assertEqual(self.client._username, 'testuser')

    @patch('gomoku.requests.post')
    def test_create_game_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "game_id": 1}
        self.client._username = "testuser"
        self.client.create_game()
        mock_post.assert_called_once_with(
            f"{self.client._server_url}/create_game",
            json={"username": "testuser"}
        )

    @patch('gomoku.requests.post')
    def test_view_board_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "board": [["~"] * 19 for _ in range(19)]
        }
        self.client._username = "testuser"
        self.client._game_id = 1
        result = self.client.view_board()
        self.assertEqual(result, "board_is_shown")

    def test_get_server_success_server(self):
        with patch('builtins.input', side_effect=["server"]):
            self.client.get_server()
        self.assertEqual(self.client._server_url, "http://109.196.98.96:8443")

    def test_get_server_success_local(self):
        with patch('builtins.input', side_effect=["local"]):
            self.client.get_server()
        self.assertEqual(self.client._server_url, "http://localhost:8443")

    def test_get_server_success_anyip(self):
        with patch('builtins.input', side_effect=["196.128.64.32"]):
            self.client.get_server()
        self.assertEqual(self.client._server_url, "http://196.128.64.32:8443")

    def test_get_server_failure(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        with patch('builtins.input', side_effect=["0.0.0..0"]):
            self.client.get_server()
        self.assertEqual(captured_output.getvalue(), '''BAD VALUE\n''')

    @patch('gomoku.requests.post')
    def test_get_ids_all_games_success(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": True, "games": list(range(10))
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.client.get_ids_all_games()
        self.assertEqual(captured_output.getvalue(),
                         f"Ids_all_games: {list(range(10))}\n")

    @patch('gomoku.requests.post')
    def test_get_ids_all_games_invalid(self, mock_post):
        mock_post.return_value.json.return_value = {
            "success": False, "message": "Invalid username"
        }
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.client.get_ids_all_games()
        self.assertEqual(captured_output.getvalue(), f"Invalid username\n")


if __name__ == '__main__':
    unittest.main()

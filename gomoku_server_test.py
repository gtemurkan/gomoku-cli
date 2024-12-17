import unittest
from unittest.mock import patch, MagicMock
from gomoku_server import GameServer
from gomoku import GomokuClient
import io
import sys

class TestGameServer(unittest.TestCase):

    def setUp(self):
        self.client = GameServer()
        self.client.SERVER_URL = "https://localhost:8443"

    def test_check_winner_first_move(self):
        board_first_move = [
                ["●", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ]
        response = self.client.check_winner(board_first_move,0,0)
        assert response == False

    def test_check_winner_winner(self):
        board_winner = [
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "○", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "○", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "○", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "○", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "●", "●", "●", "●", "●", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
                ["~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~", "~"],
            ]
        response = self.client.check_winner(board_winner,10,11)
        assert response == True
        
    def test_check_winner_draw(self):
        board_draw = [
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
                ["●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●", "○", "●"],
            ]

        response = self.client.check_winner(board_draw,10,10)
        assert response == "draw"
        

if __name__ == '__main__':
    unittest.main()

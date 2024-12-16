# gomoku-server.py

"""
Gomoku Server Implementation

This module provides a server-side implementation of the Gomoku game.
It supports:
    1. Connecting players
    2. Registering and logging in users
    3. Creating and managing games
    4. Managing game history
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import json
import ssl
import os

PORT = 8443

GAMES = {}
DATA_GAME = {}

# Load game data from a file if it exists
try:
    with open("data_game.json", "r") as f:
        DATA_GAME = json.load(f)
except FileNotFoundError:
    DATA_GAME = {"total_id_game": 0}

# Ensure the GAMES_HISTORY directory exists
if not os.path.isdir("GAMES_HISTORY"):
    os.makedirs("GAMES_HISTORY")


def save_data_game():
    """Saves the game data to a JSON file."""
    with open("data_game.json", "w") as f:
        json.dump(DATA_GAME, f)


class GameServer(BaseHTTPRequestHandler):
    """Server class handling client requests for the Gomoku game."""

    def do_POST(self):
        """Handles POST requests by routing them \
        to specific methods based on the endpoint."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        endpoints = {
            "/register": self.register_player,
            "/login": self.login_player,
            "/create_game": self.create_game,
            "/join_game": self.join_game,
            "/c_players_in_game": self.c_players_in_game,
            "/make_move": self.make_move,
            "/wait_move_second": self.wait_move_second,
            "/view_board": self.view_board,
            "/save_game_history": self.save_game_history,
            "/check_game_history": self.check_game_history,
            "/get_ids_all_games": self.get_ids_all_games,
        }

        if self.path in endpoints:
            endpoints[self.path](data)
        else:
            self.send_error(404, "Endpoint not found")

    def get_ids_all_games(self, data):
        """Gives list of all games played by user."""
        username = data.get("username")
        if username in DATA_GAME:
            self.send_json_response({
                "success": True,
                "games": DATA_GAME[username]["games"]
            })
        else:
            self.send_json_response({
                "success": False,
                "message": "Invalid username"
            })

    def save_game_history(self, GAMES, game_id):
        """Saves games' history to corresponding txt-files."""
        for user in GAMES[game_id]["players"]:
            with open(
                f'GAMES_HISTORY/'
                f'Game_{game_id}_{user}.txt',
                "a+",
                encoding="utf-8"
            ) as f:
                f.write(
                    f'PLAYERS: {GAMES[game_id]["players"][0]} - ○ ;'
                    f'{GAMES[game_id]["players"][1]} - ●\n'
                )
                for p in GAMES[game_id]["players"]:
                    if p != GAMES[game_id]["turn"]:
                        player_moved = p
                        break
                f.write(f'MADE A MOVE: {player_moved}\n')
                f.write(f'WINNER: {GAMES[game_id]["winner"]}\n')
                num_row = "".join(f"{str(ic):3}" for ic in range(1, 20))
                f.write(f'{" " * 4} {num_row}\n')
                for row in range(len(GAMES[game_id]["board"])):
                    f.write(f'{row + 1:3}| '
                            f'{"  ".join(GAMES[game_id]["board"][row])}\n')
                f.close()

    def check_game_history(self, data):
        """Checks if specified game history exists and sends date to user."""
        game_id = data.get("game_id")
        username = data.get("username")
        try:
            with open(
                    f'GAMES_HISTORY/'
                    f'Game_{game_id}_{username}.txt',
                    'r', encoding="utf-8") as file:
                data = file.readlines()
                file.close()
                self.send_json_response({
                    "success": True,
                    "data_history": data
                })
                return
        except IOError as e:
            print(e)
            self.send_json_response({
                "success": False,
                "message": (u'The file could not be opened/'
                            u'double-check the data')
            })
            return

    def send_json_response(self, response):
        """Sends a JSON-formatted response to the client."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def register_player(self, data):
        """Registers a new player with the provided username and password."""
        username = data.get("username")
        password = data.get("password")

        if username in DATA_GAME:
            self.send_json_response({
                "success": False,
                "message": "User already exists."
            })
            return

        if len(username) <= 3 or len(password) <= 3:
            self.send_json_response({
                "success": False,
                "message": ("Username and password must be "
                            "at least 4 characters long.")
            })
            return

        DATA_GAME[username] = {"password": password, "games": []}
        save_data_game()
        self.send_json_response({
            "success": True,
            "message": "User registered successfully."
        })

    def login_player(self, data):
        """Logs in an existing player by verifying credentials."""
        username = data.get("username")
        password = data.get("password")

        if username not in DATA_GAME \
                or DATA_GAME[username]["password"] != password:
            self.send_json_response({
                "success": False,
                "message": "Invalid username or password."
            })
            return

        self.send_json_response({
            "success": True,
            "message": "Login successful."
        })

    def create_game(self, data):
        """Creates a new game and assigns a unique game ID."""
        DATA_GAME["total_id_game"] += 1
        game_id = DATA_GAME["total_id_game"]
        username = data.get("username")

        GAMES[game_id] = {
            "players": [],
            "board": [["~"] * 19 for _ in range(19)],
            "turn": "",
            "winner": None
        }

        self.send_json_response({"success": True, "game_id": game_id})

    def join_game(self, data):
        """Adds a player to an existing game by game ID."""
        game_id = data.get("game_id")
        username = data.get("username")

        if username in GAMES[game_id]["players"]:
            self.send_json_response({
                "success": True,
                "message": f"Already joined game {game_id}."
            })
            return

        if game_id not in GAMES or len(GAMES[game_id]["players"]) >= 2:
            self.send_json_response({
                "success": False,
                "message": f"Cannot join game {game_id}."
            })
            return

        GAMES[game_id]["players"].append(username)
        DATA_GAME[username]["games"].append(game_id)
        if not GAMES[game_id]["turn"]:
            GAMES[game_id]["turn"] = username
        save_data_game()
        self.send_json_response({
            "success": True,
            "message": f"Joined game {game_id}."
        })

    def c_players_in_game(self, data):
        """Checks the number of players currently in a game."""
        game_id = data.get("game_id")
        players = GAMES[game_id]["players"]
        turn = GAMES[game_id]["turn"]
        success = len(players) >= 2
        self.send_json_response({
            "success": success,
            "players": players,
            "turn": turn
        })

    def view_board(self, data):
        """Returns the current game board state."""
        game_id = data.get("game_id")
        if game_id not in GAMES:
            self.send_json_response({
                "success": False,
                "message": "Invalid game."
            })
            return
        self.send_json_response({
            "success": True,
            "board": GAMES[game_id]["board"]
        })

    def wait_move_second(self, data):
        """Makes client of one player to wait for move of another player."""
        username = data.get("username")
        game_id = data.get("game_id")
        if GAMES[game_id]["turn"] == username:
            self.send_json_response({
                "success": True,
                "winner": GAMES[game_id]["winner"],
                "board": GAMES[game_id]["board"]
            })
            return
        else:
            self.send_json_response({"success": False})
            return

    def make_move(self, data):
        """Processes a player's move and updates the game state."""
        game_id = data.get("game_id")
        username = data.get("username")
        x, y = data.get("x"), data.get("y")
        game = GAMES[game_id]
        if game_id not in GAMES:
            self.send_json_response({
                "success": False,
                "message": "Invalid game."
            })
            return
        if GAMES[game_id]["winner"]:
            self.send_json_response({
                "success": True,
                "message": "Have winner.",
                "board": game["board"],
                "winner": game["winner"]
            })
            return
        if x not in range(0, 19) or y not in range(0, 19):
            self.send_json_response({
                "success": False,
                "message": "Invalid row or collumm."
            })
            return

        if game["turn"] != username:
            self.send_json_response({
                "success": False,
                "message": "Not your turn."
            })
            return

        if game["board"][x][y] != "~":
            self.send_json_response({
                "success": False,
                "message": "Cell already occupied."
            })
            return

        game["board"][x][y] = "○" \
            if game["players"].index(username) == 0 else "●"
        if game["turn"] == game["players"][0]:
            game["turn"] = game["players"][1]
        else:
            game["turn"] = game["players"][0]

        # Проверка победителя
        check_res_game = self.check_winner(game["board"], x, y)
        if check_res_game == "draw":
            game["winner"] = f'{game["players"][0]} and {game["players"][1]}'
        elif check_res_game:
            game["winner"] = username

        self.save_game_history(GAMES, game_id)
        self.send_json_response({
            "success": True,
            "board": game["board"],
            "winner": game["winner"]
        })

    def check_winner(self, board, x, y):
        c_zero_sym = 0
        for i in board:
            c_zero_sym += i.count("~")
        if c_zero_sym == 0:
            return "draw"

        def check_direction(dx, dy):
            count = 1
            for direction in (-1, 1):
                nx, ny = x + direction * dx, y + direction * dy
                while 0 <= nx < 19 \
                        and 0 <= ny < 19 \
                        and board[nx][ny] == board[x][y]:
                    count += 1
                    nx += direction * dx
                    ny += direction * dy
                if count >= 5:
                    return True
            return False

        return (check_direction(1, 0) or  # Horizontal
                check_direction(0, 1) or  # Vertical
                check_direction(1, 1) or  # Diagonal down-right
                check_direction(1, -1) or  # Diagonal down-left
                check_direction(-1, 1) or  # Diagonal up-right
                check_direction(-1, -1)  # Diagonal up-left
                )


if __name__ == "__main__":
    server_address = input(
        "Input ip_address server\n"
        "For local game input word: localhost\n"
        "\tcommand: "
    )
    try:
        server = HTTPServer((server_address, PORT), GameServer)
        # Создание SSLContext и настройка SSL
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(
            certfile="ssl_cert/server.crt", keyfile="ssl_cert/server.key")

        # Применение SSLContext к сокету сервера
        server.socket = context.wrap_socket(server.socket, server_side=True)
        print(f"Server running on port {PORT}...")
        server.serve_forever()
    except socket.gaierror as e:
        print('Failed. Try again')

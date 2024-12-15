from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = 8080

GAMES = {}
DATA_GAME = {}

# Загружаем игроков из файла
try:
    with open("data_game.json", "r") as f:
        DATA_GAME = json.load(f)
except FileNotFoundError:
    DATA_GAME = {"total_id_game": 0}

# Проверяем или создаем папку GAMES_HISTORY
if not os.path.isdir("GAMES_HISTORY"):
    os.makedirs("GAMES_HISTORY")


def save_data_game():
    with open("data_game.json", "w") as f:
        json.dump(DATA_GAME, f)


class GameServer(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        if self.path == "/register":
            self.register_player(data)
        elif self.path == "/login":
            self.login_player(data)
        elif self.path == "/create_game":
            self.create_game(data)
        elif self.path == "/join_game":
            self.join_game(data)
        elif self.path == "/c_players_in_game":
            self.c_players_in_game(data)
        elif self.path == "/make_move":
            self.make_move(data)
        elif self.path == "/wait_move_second":
            self.wait_move_second(data)
        elif self.path == "/view_board":
            self.view_board(data)
        elif self.path == "/save_game_history":
            self.save_game_history(data)
        elif self.path == "/check_game_history":
            self.check_game_history(data)
        elif self.path == "/get_ids_all_games":
            self.get_ids_all_games(data)
        else:
            self.send_error(404, "Endpoint not found")

    def get_ids_all_games(self,data):
        username = data.get("username")
        if username in DATA_GAME:
            self.send_json_response({"success": True, "games": DATA_GAME[username]["games"]})
        else:
            self.send_json_response({"success": False, "message": "Invalid username"})


    def save_game_history(self,GAMES,game_id):
        for user in GAMES[game_id]["players"]:
            with open(f'GAMES_HISTORY/Game_{game_id}_{user}.txt', "a+", encoding="utf-8") as f:
                f.write(f'PLAYERS: {GAMES[game_id]["players"][0]} - ○ ; {GAMES[game_id]["players"][1]} - ●\n')
                f.write(f'MADE A MOVE: {[el for el in GAMES[game_id]["players"] if el != GAMES[game_id]["turn"]][0]}\n')
                f.write(f'WINNER: {GAMES[game_id]["winner"]}\n')
                f.write(f'{" " * 4} {"".join([f"{str(int_columm):3}" for int_columm in range(1, 20)])}\n')
                for row in range(len(GAMES[game_id]["board"])):
                    f.write(f'{row + 1:3}| {"  ".join(GAMES[game_id]["board"][row])}\n')
                f.close()

    def check_game_history(self,data):
        game_id = data.get("game_id")
        username = data.get("username")

        try:
            with open(f'GAMES_HISTORY/Game_{game_id}_{username}.txt', 'r', encoding="utf-8") as file:
                data = file.readlines()
                file.close()
                self.send_json_response({"success": True, "data_history": data})
                return
        except IOError as e:
            print(e)
            self.send_json_response({"success": False, "message": u'The file could not be opened/double-check the data'})
            return


    def send_json_response(self, response):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode("utf-8"))

    def register_player(self, data):
        username = data.get("username")
        password = data.get("password")

        if username in DATA_GAME:
            self.send_json_response({"success": False, "message": "User already exists."})
            return
        if len(username)<=3 or len(password)<=3:
            self.send_json_response({"success": False, "message": "Login and Password lengths must be more than 3"})
            return

        DATA_GAME[username] = {"password": password, "games": []}
        save_data_game()
        self.send_json_response({"success": True, "message": "User registered successfully."})

    def login_player(self, data):
        username = data.get("username")
        password = data.get("password")

        if username not in DATA_GAME or DATA_GAME[username]["password"] != password:
            self.send_json_response({"success": False, "message": "Invalid username or password."})
            return

        self.send_json_response({"success": True, "message": "Login successful."})

    def create_game(self, data):
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
        game_id = data.get("game_id")
        username = data.get("username")

        if username in GAMES[game_id]["players"]:
            self.send_json_response({"success": True, "message": f'Already join game {game_id}.'})
            return

        if game_id not in GAMES or len(GAMES[game_id]["players"]) >= 2:
            self.send_json_response({"success": False, "message": f'Cannot join game {game_id}.'})
            return

        GAMES[game_id]["players"].append(username)
        DATA_GAME[username]["games"].append(game_id)
        if GAMES[game_id]["turn"] == "":
            GAMES[game_id]["turn"] = username
        save_data_game()
        self.send_json_response({"success": True, "message": f'Joined game {game_id}.'})
    def c_players_in_game(self,data):
        game_id = data.get("game_id")
        if len(GAMES[game_id]["players"]) < 2:
            self.send_json_response({"success": False, "players": GAMES[game_id]["players"], "turn": GAMES[game_id]["turn"]})
            return
        else:
            self.send_json_response({"success": True, "players": GAMES[game_id]["players"], "turn": GAMES[game_id]["turn"]})
            return


    def view_board(self, data):
        game_id = data.get("game_id")

        if game_id not in GAMES:
            self.send_json_response({"success": False, "message": "Invalid game.", "board": GAMES[game_id]["board"]})
            return
        if GAMES[game_id]["winner"]:
            self.send_json_response({"success": False, "message": "Have winner.", "board": GAMES[game_id]["board"]})
            return

        self.send_json_response({"success": True, "board": GAMES[game_id]["board"]})
        return

    def wait_move_second(self,data):
        username = data.get("username")
        game_id = data.get("game_id")
        if GAMES[game_id]["turn"] == username:
            self.send_json_response({"success": True, "winner": GAMES[game_id]["winner"], "board": GAMES[game_id]["board"]})
            return
        else:
            self.send_json_response({"success": False})
            return

    def make_move(self, data):
        game_id = data.get("game_id")
        username = data.get("username")
        x, y = data.get("x"), data.get("y")
        game = GAMES[game_id]


        if game_id not in GAMES:
            self.send_json_response({"success": False, "message": "Invalid game."})
            return
        if GAMES[game_id]["winner"]:

            self.send_json_response({"success": True, "message": "Have winner.", "board": game["board"], "winner": game["winner"]})
            return
        if x not in ([i for i in range(0,19)]) or y not in ([i for i in range(0,19)]):
            self.send_json_response({"success": False, "message": "Invalid row or collumm."})
            return

        if game["turn"] != username:
            self.send_json_response({"success": False, "message": "Not your turn."})
            return

        if game["board"][x][y] != "~":
            self.send_json_response({"success": False, "message": "Cell already occupied."})
            return

        game["board"][x][y] = "○" if game["players"].index(username) == 0 else "●"
        game["turn"] = game["players"][1] if game["turn"] == game["players"][0] else game["players"][0]

        # Проверка победителя
        check_res_game=self.check_winner(game["board"], x, y)
        if check_res_game == "draw":
            game["winner"] = f'{game["players"][0]} and {game["players"][1]}'
        elif check_res_game:
            game["winner"] = username

        self.save_game_history(GAMES,game_id)
        self.send_json_response({"success": True, "board": game["board"], "winner": game["winner"]})

    def check_winner(self, board, x, y):
        c_zero_sym=0
        for i in board:
            c_zero_sym+=i.count("~")
        if c_zero_sym==0:
            return "draw"

        def check_direction(dx, dy):
            count = 1
            for direction in (-1, 1):
                nx, ny = x + direction * dx, y + direction * dy
                while 0 <= nx < 19 and 0 <= ny < 19 and board[nx][ny] == board[x][y]:
                    count += 1
                    nx += direction * dx
                    ny += direction * dy
                if count >= 5:
                    return True
            return False

        return (check_direction(1, 0) or  # Horizontal
                check_direction(0, 1) or  # Vertical
                check_direction(1, 1) or  # Diagonal down-right
                check_direction(1, -1) or # Diagonal down-left
                check_direction(-1, 1) or # Diagonal up-right
                check_direction(-1, -1) #Diagonal up-left
                )
if __name__ == "__main__":
    server_address=input("Input ip_address server\nFor local game input word: localhost\n    command: ")
    server = HTTPServer((server_address, PORT), GameServer)
    print(f"Server running on port {PORT}...")
    server.serve_forever()

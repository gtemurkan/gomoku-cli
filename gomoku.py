# gomoku.py

"""This module must be for gomoku game.  """

import requests
import time
import os
import re


class GomokuClient:
    def __init__(self):
        """Initialize GomokuClient

        username
        """
        self.username = None
        self.game_id = None
        self.SERVER_URL = None

    def slogan_gomoku(self):
        """Print 'Gomoku' in CLI style"""
        print(r'''
      ____                           _
     / ___|  ___   _ __ ___    ___  | | __ _   _
    | |  _  / _ \ | '_ ` _ \  / _ \ | |/ /| | | |
    | |_| || (_) || | | | | || (_) ||   < | |_| |
     \____| \___/ |_| |_| |_| \___/ |_|\_\ \__,_|

''')

    def get_server(self):
        """Interactively asks user for server url"""
        IP_PATTERN = (r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.)){3}"
                        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" "{1}$")
        while True:
            ans_server_url = input('''
To play on a local network, Enter word: <local>
To play on the official server, Enter word: <server>
If you want to play on an unofficial server, Enter IP address of that server
    command: ''')

            if ans_server_url in ["server", "<server>"]:
                self.SERVER_URL = "http://109.196.98.96:8080"
                break
            if ans_server_url in ["local", "<local>"]:
                self.SERVER_URL = "http://localhost:8080"
                break
            if bool(re.match(IP_PATTERN, ans_server_url)):
                self.SERVER_URL = ans_server_url
                break
            else:
                print("BAD VALUE")

    def register(self):
        os.system('cls')
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(f"{self.SERVER_URL}/register", json={"username": username, "password": password})
        print(response.json()["message"])

    def login(self):
        os.system('cls')
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(f"{self.SERVER_URL}/login", json={"username": username, "password": password})
        if response.json()["success"]:
            self.username = username
        print(response.json()["message"])

    def get_ids_all_games(self):
        if self.username:
            response = requests.post(f"{self.SERVER_URL}/get_ids_all_games", json={"username": self.username})
            if response.json()["success"]:
                os.system('cls')
                print(f"Ids_all_games: {response.json()['games']}")
            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print("Please Login or Register\nIf you're registered, you need to login")
    def create_game(self):
        if self.username:
            response = requests.post(f"{self.SERVER_URL}/create_game", json={"username": self.username})
            if response.json()["success"]:
                os.system('cls')
                print(f"Game created with ID: {response.json()['game_id']}")
            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print("Please Login or Register\nIf you're registered, you need to login")

    def check_game_history(self):
        """Checks game history"""
        if self.username:
            os.system('cls')
            self.game_id = input("Enter the number of the game you are interested in, in which you participated: ")
            response = requests.post(f"{self.SERVER_URL}/check_game_history", json={"username": self.username, "game_id": self.game_id})
            if response.json()["success"]:

                self.data = response.json()["data_history"]
                exit_check=True
                while exit_check:
                    print("1. Write the number of the move you are interested in (starts from 1)\n Write <exit> to return to the menu")
                    print(f'Total moves: {len(self.data)//23}')
                    ans=input("Enter: ")
                    os.system('cls')
                    print(f'MOVE: {ans}')
                    if ans in ["exit","<exit>"]:
                        break
                    try:
                        i=int(ans)-1
                        for line in range(23*i,23*(i+1)):
                            print(self.data[line][:-1])
                    except:
                        print("Invalid Value")

            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print("Please Login or Register\nIf you're registered, you need to login")

    def join_game(self):
        if self.username:
            self.game_id = int(input("Enter game ID to join: "))
            os.system('cls')
            response = requests.post(f"{self.SERVER_URL}/join_game", json={"username": self.username, "game_id": self.game_id})
            print(response.json()["message"])
            c_wainting = 1
            while True:
                print(f'Wait 10 seconds for second user')
                time.sleep(10)
                response = requests.post(f"{self.SERVER_URL}/c_players_in_game", json={"game_id": self.game_id})
                data = response.json()
                if data["success"]:
                    if data["turn"] == self.username:
                        os.system('cls')
                        print(f'You and {[el for el in data["players"] if el != self.username][0]} in the game')
                        print("Your turn\nLet's make  move")
                    else:
                        os.system('cls')
                        print(f'You and {[el for el in data["players"] if el != self.username][0]} in the game')
                        print("Not your turn\nLet's wait opponent's move")
                        c_wainting = 1
                        while True:
                            print(f'Wait {2.5*c_wainting} seconds for second user')
                            time.sleep(2.5*c_wainting)
                            response = requests.post(f"{self.SERVER_URL}/wait_move_second", json={"username": self.username, "game_id": self.game_id})
                            data = response.json()
                            if data["success"]:
                                os.system('cls')
                                print(f'Your opponent has made a move.')
                                break
                            else:
                                if c_wainting % 6 == 0:
                                    os.system('cls')
                                    want_exit = input("Second user hasn't made a move yet\nIf you want to continue waiting write <cont>\nIf you wait exit write <exit>\n command: ")
                                    if want_exit in ["<cont>", "cont"]:

                                        continue
                                    elif want_exit in ["<exit>", "exit"]:
                                        os.system('cls')
                                        break
                                    else:
                                        print("Write only <cont> or <exit>")
                                else:
                                    c_wainting += 1
                    break
                elif c_wainting % 6 == 0:
                    os.system('cls')
                    want_exit = input("Second user not connected yet\nIf you want to continue waiting write <cont>\nIf you wait exit write <exit>\n command: ")
                    if want_exit in ["<cont>", "cont"]:

                        continue
                    elif want_exit in ["<exit>", "exit"]:
                        os.system('cls')
                        break
                    else:
                        print("Write only <cont> or <exit>")
                else:
                    c_wainting += 1

        else:
            os.system('cls')
            print("Please Login or Register\nIf you're registered, you need to login")


    def view_board(self):
        response = requests.post(f"{self.SERVER_URL}/view_board", json={"username": self.username, "game_id": self.game_id})
        data = response.json()
        if data["success"]:
            os.system('cls')
            print(f'{" "*4} {"".join([f"{str(int_columm):3}" for int_columm in range(1,20)])}')
            for row in range(len(data["board"])):
                print(f'{row+1:3}| {"  ".join(data["board"][row])}')
            return "board_is_shown"
        else:
            return data["message"]

    def make_move(self):
        if self.game_id and self.username:
            x=None
            y=None
            res_view=GomokuClient.view_board(self)
            if res_view == "board_is_shown":
                try:
                    x = int(input("Enter row (1-19): "))
                    y = int(input("Enter column (1-19): "))
                    response = requests.post(f"{self.SERVER_URL}/make_move", json={"username": self.username, "game_id": self.game_id, "x": x-1, "y": y-1})
                except:
                    response = requests.post(f"{self.SERVER_URL}/make_move", json={"username": self.username, "game_id": self.game_id, "x": x, "y": y})
            else:
                response = requests.post(f"{self.SERVER_URL}/make_move", json={"username": self.username, "game_id": self.game_id, "x": x, "y": y})
            data = response.json()
            if data["success"]:
                os.system('cls')
                print(f'{" "*4} {"".join([f"{str(int_columm):3}" for int_columm in range(1,20)])}')
                for row in range(len(data["board"])):
                    print(f'{row+1:3}| {"  ".join(data["board"][row])}')
                if res_view == "board_is_shown":
                    print("Move successful!")
                if data["winner"]:
                    for _ in range(3):
                        print(f"Winner: {data['winner']}")
                else:
                    c_wainting = 1
                    while True:
                        print(f'Wait {2.5*(c_wainting)} seconds for second user')
                        time.sleep(2.5*c_wainting)
                        response = requests.post(f"{self.SERVER_URL}/wait_move_second", json={"username": self.username, "game_id": self.game_id})
                        data = response.json()
                        if data["success"]:
                            if data["winner"]:
                                os.system('cls')
                                print(f'{" " * 4} {"".join([f"{str(int_columm):3}" for int_columm in range(1, 20)])}')
                                for row in range(len(data["board"])):
                                    print(f'{row + 1:3}| {"  ".join(data["board"][row])}')
                                for _ in range(3):
                                    print(f"Winner: {data['winner']}")

                            else:
                                os.system('cls')
                                print(f'Your opponent has made a move.')
                            break
                        else:
                            if c_wainting % 6 == 0:
                                want_exit = input("Second user hasn't made a move yet\nIf you want to continue waiting write <cont>\nIf you wait exit write <exit>\n command: ")
                                if want_exit in ["<cont>", "cont"]:
                                    c_wainting += 1
                                    os.system('cls')
                                    continue
                                if want_exit in ["<exit>", "exit"]:
                                    os.system('cls')
                                    break
                            c_wainting += 1
            else:
                os.system('cls')
                print(data["message"])
        elif self.username:
            os.system('cls')
            print("Please join game (point 4)")
        else:
            os.system('cls')
            print("Please Login or Register\nIf you're registered, you need to login")


if __name__ == "__main__":
    client = GomokuClient()
    os.system('cls')

    client.get_server()

    os.system('cls')

    client.slogan_gomoku()

    while True:
        try:
            print("\n1. Register\n2. Login\n3. Create Game\n4. Join Game\n5. Make Move\n6. Check game history\n7. Get ids all games\n8. Exit")
            choice = input("Select an option: ")
            match choice:
                case "1":
                    client.register()
                case "2":
                    client.login()
                case "3":
                    client.create_game()
                case "4":
                    client.join_game()
                case "5":
                    client.make_move()
                case "6":
                    client.check_game_history()
                case "7":
                    client.get_ids_all_games()
                case "8":
                    break
                case _:
                    print("Invalid choice. Try again.")
        except ConnectionError:
            print("Проверьте доступ к сети\nИли обратитесь к администратору сервера")
        except Exception as e:
            print(f"{type(e).__name__}\nError: {e}")

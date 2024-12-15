# gomoku.py

"""
Gomoku Client Implementation

This module provides a client-side implementation of the Gomoku game.
It supports:
    1. Connecting to the game server
    2. Registering and logging in users
    3. Creating and joining games
    4. Making moves and viewing the game board
    5. Checking game history
"""

import requests
import time
import os
import re


class GomokuClient:
    """
    Client class for interacting with the Gomoku game server.
    
    Attributes:
    
    """

    def __init__(self):
        """
        Initializes the client with default values,
        such as username and server URL.
        """
        self.username = None
        """For internal use"""
        self.game_id = None
        """For internal use"""
        self.SERVER_URL = None
        """For internal use"""
        self.__NUM_ROW = "".join(f"{str(ic):3}" for ic in range(1, 20))

    def slogan_gomoku(self):
        """Displays the ASCII art slogan of the game."""
        print(r'''
      ____                           _
     / ___|  ___   _ __ ___    ___  | | __ _   _
    | |  _  / _ \ | '_ ` _ \  / _ \ | |/ /| | | |
    | |_| || (_) || | | | | || (_) ||   < | |_| |
     \____| \___/ |_| |_| |_| \___/ |_|\_\ \__,_|

''')

    def get_server(self):
        """Prompts the user to select a server or enter a custom server URL.

        Supports three options:
            - Local server
            - Official server
            - Custom server IP address
        """
        IP_PATTERN = (
            r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.)){3}"
            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" "{1}$"
        )
        while True:
            ans_server_url = input('''
To play on a local network, Enter word: <local>
To play on the official server, Enter word: <server>
If you want to play on an unofficial server, Enter IP address of that server
    command: ''')

            requests.packages.urllib3.disable_warnings()

            if ans_server_url in ["server", "<server>"]:
                self.SERVER_URL = "https://109.196.98.96:8443"
                break
            if ans_server_url in ["local", "<local>"]:
                self.SERVER_URL = "https://localhost:8443"
                break
            if bool(re.match(IP_PATTERN, ans_server_url)):
                self.SERVER_URL = ans_server_url
                break
            else:
                print("BAD VALUE")

    def register(self):
        """Registers a new user by sending their credentials to the server."""
        os.system('cls')
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(
            f"{self.SERVER_URL}/register",
            json={"username": username, "password": password},
            verify=False
        )
        print(response.json()["message"])

    def login(self):
        """
        Logs in an existing user by verifying
        credentials with the server.
        """
        os.system('cls')
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(
            f"{self.SERVER_URL}/login",
            json={"username": username, "password": password},
            verify=False
        )
        if response.json()["success"]:
            self.username = username
        print(response.json()["message"])

    def get_ids_all_games(self):
        """Displays ids of all games user played"""
        if self.username:
            response = requests.post(
                f"{self.SERVER_URL}/get_ids_all_games",
                json={"username": self.username},
                verify=False
            )
            if response.json()["success"]:
                os.system('cls')
                print(f"Ids_all_games: {response.json()['games']}")
            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print(
                "Please Login or Register\n"
                "If you're registered, you need to login"
            )

    def create_game(self):
        """
        Creates a new game session and
        retrieves its game ID from the server.
        """
        if self.username:
            response = requests.post(
                f"{self.SERVER_URL}/create_game",
                json={"username": self.username},
                verify=False
            )
            if response.json()["success"]:
                os.system('cls')
                print(f"Game created with ID: {response.json()['game_id']}")
            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print(
                "Please Login or Register\n"
                "If you're registered, you need to login"
            )

    def check_game_history(self):
        """
        Interactively shows which moves were
        made in selected game. Player may choose specific moves.
        """
        if self.username:
            os.system('cls')
            self.game_id = input(
                "Enter the number of the game you are "
                "interested in, in which you participated: "
            )
            response = requests.post(
                f"{self.SERVER_URL}/check_game_history",
                json={"username": self.username, "game_id": self.game_id},
                verify=False
            )
            if response.json()["success"]:

                self.__data = response.json()["data_history"]
                exit_check = True
                while exit_check:
                    print(
                        "1. Write the number of the move "
                        "you are interested in (starts from 1)\n "
                        "Write <exit> to return to the menu"
                    )
                    print(f'Total moves: {len(self.__data)//23}')
                    ans = input("Enter: ")
                    os.system('cls')
                    print(f'MOVE: {ans}')
                    if ans in ["exit", "<exit>"]:
                        break
                    try:
                        i = int(ans) - 1
                        for line in range(23 * i, 23 * (i + 1)):
                            print(self.__data[line][:-1])
                    except ValueError:
                        print("Invalid Value")

            else:
                os.system('cls')
                print(response.json()["message"])
        else:
            os.system('cls')
            print("Please Login or Register\n"
                  "If you're registered, you need to login")

    def join_game(self):
        """Joins user to an existing game with specified ID"""
        if self.username:
            self.game_id = int(input("Enter game ID to join: "))
            os.system('cls')
            response = requests.post(
                f"{self.SERVER_URL}/join_game",
                json={"username": self.username,
                      "game_id": self.game_id},
                verify=False
            )
            print(response.json()["message"])
            c_wainting = 1
            while True:
                print(f'Wait 10 seconds for second user')
                time.sleep(10)
                response = requests.post(
                    f"{self.SERVER_URL}/c_players_in_game",
                    json={"game_id": self.game_id},
                    verify=False
                )
                data = response.json()
                if data["success"]:
                    for p in data["players"]:
                        if p != self.username:
                            opponent = p
                            break
                    os.system('cls')
                    print(f'You and {opponent} in the game')
                    if data["turn"] == self.username:
                        print("Your turn\nLet's make  move")
                    else:
                        print("Not your turn\nLet's wait opponent's move")
                        c_wainting = 1
                        while True:
                            print(f'Wait {2.5 * c_wainting}'
                                  'seconds for second user')
                            time.sleep(2.5*c_wainting)
                            response = requests.post(
                                f"{self.SERVER_URL}/wait_move_second",
                                json={"username": self.username,
                                      "game_id": self.game_id},
                                verify=False
                            )
                            data = response.json()
                            if data["success"]:
                                os.system('cls')
                                print(f'Your opponent has made a move.')
                                break
                            else:
                                if c_wainting % 6 == 0:
                                    os.system('cls')
                                    want_exit = input(
                                        "Second user hasn't made a move yet\n"
                                        "If you want to continue waiting "
                                        "write <cont>\nIf you wait exit "
                                        "write <exit>\n command: ")
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
                    want_exit = input(
                        "Second user not connected yet\n"
                        "If you want to continue waiting write <cont>\n"
                        "If you wait exit write <exit>\n command: "
                    )
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
            print("Please Login or Register\n"
                  "If you're registered, you need to login")

    def view_board(self):
        """
        Print an ASCII Picture of current
        game state including players pieces
        """
        response = requests.post(
            f"{self.SERVER_URL}/view_board",
            json={"username": self.username,
                  "game_id": self.game_id},
            verify=False
        )
        data = response.json()
        if data["success"]:
            os.system('cls')
            print(f'{" " * 4} {self.__NUM_ROW}')
            for row in range(len(data["board"])):
                print(f'{row+1:3}| {"  ".join(data["board"][row])}')
            return "board_is_shown"
        else:
            return data["message"]

    def make_move(self):
        """
        Interactively asks player for row and
        column of place where theirs' piece should
        be placed. Validated the move.
        """
        if self.game_id and self.username:
            x = None
            y = None
            res_view = GomokuClient.view_board(self)
            if res_view == "board_is_shown":
                try:
                    x = int(input("Enter row (1-19): "))
                    y = int(input("Enter column (1-19): "))
                    response = requests.post(
                        f"{self.SERVER_URL}/make_move",
                        json={"username": self.username,
                              "game_id": self.game_id, "x": x-1, "y": y-1},
                        verify=False
                    )
                except:
                    response = requests.post(
                        f"{self.SERVER_URL}/make_move",
                        json={"username": self.username,
                              "game_id": self.game_id, "x": x, "y": y},
                        verify=False
                    )
            else:
                response = requests.post(
                    f"{self.SERVER_URL}/make_move",
                    json={"username": self.username,
                          "game_id": self.game_id, "x": x, "y": y},
                    verify=False
                )
            data = response.json()
            if data["success"]:
                os.system('cls')
                print(f'{" " * 4} {self.__NUM_ROW}')
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
                        print(f'Wait {2*(c_wainting)} seconds for second user')
                        time.sleep(2*c_wainting)
                        response = requests.post(
                            f"{self.SERVER_URL}/wait_move_second",
                            json={"username": self.username,
                                  "game_id": self.game_id},
                            verify=False
                        )
                        data = response.json()
                        if data["success"]:
                            if data["winner"]:
                                os.system('cls')
                                print(f'{" " * 4} {self.__NUM_ROW}')
                                for row in range(len(data["board"])):
                                    print(f'{row + 1:3}| '
                                          '{"  ".join(data["board"][row])}')
                                for _ in range(3):
                                    print(f"Winner: {data['winner']}")

                            else:
                                os.system('cls')
                                print(f'Your opponent has made a move.')
                            break
                        else:
                            if c_wainting % 6 == 0:
                                want_exit = input(
                                    "Second user hasn't made a move yet\n"
                                    "If you want to continue waiting write "
                                    "<cont>\nIf you wait exit write <exit>\n "
                                    "command: ")
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
            print("Please Login or Register\n"
                  "If you're registered, you need to login")


if __name__ == "__main__":
    client = GomokuClient()
    os.system('cls')

    client.get_server()

    os.system('cls')

    client.slogan_gomoku()

    while True:
        try:
            print(
                "\n1. Register"
                "\n2. Login"
                "\n3. Create Game"
                "\n4. Join Game"
                "\n5. Make Move"
                "\n6. Check game history"
                "\n7. Get ids all games"
                "\n8. Exit"
            )
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
            print("Check your internet connection\n"
                  "Or ask for help your server administrator")
        except Exception as e:
            print(f"{type(e).__name__}\nError: {e}")

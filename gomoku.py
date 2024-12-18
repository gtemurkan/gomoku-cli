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


_clear = None


class GomokuClient:
    """
    Client class for interacting with the Gomoku game server.
    """

    def __init__(self):
        """
        Initializes the client with default values,
        such as username and server URL.
        """
        self._username = None
        self._game_id = None
        self._server_url = None
        self.__NUM_ROW = "".join(f"{str(ic):3}" for ic in range(1, 20))

    def slogan_gomoku(self):
        """Displays the ASCII art slogan of the game."""
        print(
            r"""
      ____                           _
     / ___|  ___   _ __ ___    ___  | | __ _   _
    | |  _  / _ \ | '_ ` _ \  / _ \ | |/ /| | | |
    | |_| || (_) || | | | | || (_) ||   < | |_| |
     \____| \___/ |_| |_| |_| \___/ |_|\_\ \__,_|

"""
        )

    def get_server(self):
        """Prompts the user to select a server or enter a custom server URL.

        Supports three options:
            - Local server
            - Official server
            - Custom server IP address
        """
        IP_PATTERN = (
            r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.)){3}"
            r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"
            "{1}$"
        )

        ans_server_url = input(
            "To play on a local network, Enter word: <local>\n"
            "To play on the official server, Enter word: <server>\n"
            "If you want to play on an unofficial server,"
            "enter IP address of that server\n"
            "\tCommand: "
        )

        if ans_server_url in ["server", "<server>"]:
            self._server_url = "http://109.196.98.96:8443"
            return True
        if ans_server_url in ["local", "<local>"]:
            self._server_url = "http://localhost:8443"
            return True
        if bool(re.match(IP_PATTERN, ans_server_url)):
            self._server_url = f"http://{ans_server_url}:8443"
            return True
        else:
            print("BAD VALUE")
            return False

    # Borrowed method example for class GomokuClient - begin
    def register(self):
        """
        Registers a new user by sending their credentials to the server.
        """
        _clear()
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(
            f"{self._server_url}/register",
            json={"username": username, "password": password}
        )
        print(response.json()["message"])
    # Borrowed method example for class GomokuClient - end

    def login(self):
        """
        Logs in an existing user by verifying
        credentials with the server.
        """
        _clear()
        username = input("Enter username: ")
        password = input("Enter password: ")
        response = requests.post(
            f"{self._server_url}/login",
            json={"username": username, "password": password}
        )
        if response.json()["success"]:
            self._username = username
        print(response.json()["message"])

    def get_ids_all_games(self):
        """Displays ids of all games user played"""
        if self._username:
            response = requests.post(
                f"{self._server_url}/get_ids_all_games",
                json={"username": self._username}
            )
            if response.json()["success"]:
                _clear()
                print(f"Ids_all_games: {response.json()['games']}")
            else:
                _clear()
                print(response.json()["message"])
        else:
            _clear()
            print(
                "Please Login or Register\n" "If you're registered, you need to login"
            )

    def create_game(self):
        """
        Creates a new game session and
        retrieves its game ID from the server.
        """
        if self._username:
            response = requests.post(
                f"{self._server_url}/create_game",
                json={"username": self._username}
            )
            if response.json()["success"]:
                _clear()
                print(f"Game created with ID: {response.json()['game_id']}")
            else:
                _clear()
                print(response.json()["message"])
        else:
            _clear()
            print(
                "Please Login or Register\n" "If you're registered, you need to login"
            )

    def check_game_history(self):
        """
        Interactively shows which moves were
        made in selected game. Player may choose specific moves.
        """
        if self._username:
            _clear()
            self._game_id = input(
                "Enter the number of the game you are "
                "interested in, in which you participated: "
            )
            response = requests.post(
                f"{self._server_url}/check_game_history",
                json={"username": self._username, "game_id": self._game_id}
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
                    print(f"Total moves: {len(self.__data)//23}")
                    ans = input("Enter: ")
                    _clear()
                    print(f"MOVE: {ans}")
                    if ans in ["exit", "<exit>"]:
                        break
                    try:
                        i = int(ans) - 1
                        for line in range(23 * i, 23 * (i + 1)):
                            print(self.__data[line][:-1])
                    except ValueError:
                        print("Invalid Value")

            else:
                _clear()
                print(response.json()["message"])
        else:
            _clear()
            print(
                "Please Login or Register\n" "If you're registered, you need to login"
            )

    def join_game(self):
        """Joins user to an existing game with specified ID"""
        if self._username:
            self._game_id = int(input("Enter game ID to join: "))
            _clear()
            response = requests.post(
                f"{self._server_url}/join_game",
                json={"username": self._username, "game_id": self._game_id}
            )
            print(response.json()["message"])
            c_waiting = 1
            while True:
                print(f"Wait 2 seconds for second user")
                time.sleep(2)
                response = requests.post(
                    f"{self._server_url}/c_players_in_game",
                    json={"game_id": self._game_id}
                )
                data = response.json()
                if data["success"]:
                    for p in data["players"]:
                        if p != self._username:
                            opponent = p
                            break
                    _clear()
                    print(f"You and {opponent} in the game")
                    if data["turn"] == self._username:
                        print("Your turn\nLet's make  move")
                    else:
                        print("Not your turn\nLet's wait opponent's move")
                        c_waiting = 1
                        while True:
                            print(
                                f"Wait {2 * c_waiting}" "seconds for second user")
                            time.sleep(2 * c_waiting)
                            response = requests.post(
                                f"{self._server_url}/wait_move_second",
                                json={
                                    "username": self._username,
                                    "game_id": self._game_id,
                                }
                            )
                            data = response.json()
                            if data["success"]:
                                _clear()
                                print(f"Your opponent has made a move.")
                                break
                            else:
                                if c_waiting % 6 == 0:
                                    _clear()
                                    want_exit = input(
                                        "Second user hasn't made a move yet\n"
                                        "If you want to continue waiting "
                                        "write <cont>\nIf you wait exit "
                                        "write <exit>\n command: "
                                    )
                                    if want_exit in ["<cont>", "cont"]:
                                        c_waiting = 1
                                        continue
                                    elif want_exit in ["<exit>", "exit"]:
                                        _clear()
                                        break
                                    else:
                                        print("Write only <cont> or <exit>")
                                else:
                                    c_waiting += 1
                    break
                elif c_waiting % 6 == 0:
                    _clear()
                    want_exit = input(
                        "Second user not connected yet\n"
                        "If you want to continue waiting write <cont>\n"
                        "If you wait exit write <exit>\n command: "
                    )
                    if want_exit in ["<cont>", "cont"]:
                        c_waiting = 1
                        continue
                    elif want_exit in ["<exit>", "exit"]:
                        _clear()
                        break
                    else:
                        print("Write only <cont> or <exit>")
                else:
                    c_waiting += 1

        else:
            _clear()
            print(
                "Please Login or Register\n" "If you're registered, you need to login"
            )

    def view_board(self):
        """
        Print an ASCII Picture of current
        game state including players pieces
        """
        response = requests.post(
            f"{self._server_url}/view_board",
            json={"username": self._username, "game_id": self._game_id}
        )
        data = response.json()
        if data["success"]:
            _clear()
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
        if self._game_id and self._username:
            x = None
            y = None
            res_view = GomokuClient.view_board(self)
            if res_view == "board_is_shown":
                try:
                    x = int(input("Enter row (1-19): "))
                    y = int(input("Enter column (1-19): "))
                    response = requests.post(
                        f"{self._server_url}/make_move",
                        json={
                            "username": self._username,
                            "game_id": self._game_id,
                            "x": x - 1,
                            "y": y - 1,
                        }
                    )
                except:
                    response = requests.post(
                        f"{self._server_url}/make_move",
                        json={
                            "username": self._username,
                            "game_id": self._game_id,
                            "x": x,
                            "y": y,
                        }
                    )
            else:
                response = requests.post(
                    f"{self._server_url}/make_move",
                    json={
                        "username": self._username,
                        "game_id": self._game_id,
                        "x": x,
                        "y": y,
                    }
                )
            data = response.json()
            if data["success"]:
                _clear()
                print(f'{" " * 4} {self.__NUM_ROW}')
                for row in range(len(data["board"])):
                    print(f'{row+1:3}| {"  ".join(data["board"][row])}')
                if res_view == "board_is_shown":
                    print("Move successful!")
                if data["winner"]:
                    for _ in range(3):
                        print(f"Winner: {data['winner']}")
                else:
                    c_waiting = 1
                    while True:
                        print(f"Wait {2*(c_waiting)} seconds for second user")
                        time.sleep(2 * c_waiting)
                        response = requests.post(
                            f"{self._server_url}/wait_move_second",
                            json={"username": self._username,
                                  "game_id": self._game_id}
                        )
                        data = response.json()
                        if data["success"]:
                            if data["winner"]:
                                _clear()
                                print(f'{" " * 4} {self.__NUM_ROW}')
                                for row in range(len(data["board"])):
                                    print(
                                        f'{row +
                                            1:3}| {"  ".join(data["board"][row])}'
                                    )
                                for _ in range(3):
                                    print(f"Winner: {data['winner']}")

                            else:
                                _clear()
                                print(f"Your opponent has made a move.")
                            break
                        else:
                            if c_waiting % 6 == 0:
                                want_exit = input(
                                    "Second user hasn't made a move yet\n"
                                    "If you want to continue waiting write "
                                    "<cont>\nIf you wait exit write <exit>\n "
                                    "command: "
                                )
                                if want_exit in ["<cont>", "cont"]:
                                    c_waiting = 1
                                    _clear()
                                    continue
                                if want_exit in ["<exit>", "exit"]:
                                    _clear()
                                    break
                            c_waiting += 1
            else:
                _clear()
                print(data["message"])
        elif self._username:
            _clear()
            print("Please join game (point 4)")
        else:
            _clear()
            print(
                "Please Login or Register\n" "If you're registered, you need to login"
            )


def main():
    """
    Starting point for the gomoku client script.
    """

    global _clear
    
    if os.name == 'nt':
        _clear = lambda: os.system('cls')
    else:
        _clear = lambda: os.system('clear')

    client = GomokuClient()
    _clear()

    if not client.get_server():
        print("The script will end in 10 seconds.")
        time.sleep(10)
        exit()

    _clear()

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
            print(
                "Check your internet connection\n"
                "Or ask for help your server administrator"
            )
        except Exception as e:
            print(f"{type(e).__name__}\nError: {e}")


if __name__ == "__main__":
    main()

import sys

try:
    from commands import *
except ImportError:
    import os
    os.system("pip install git+https://github.com/egigoka/commands")
    from commands import *
try:
    import trello
except ImportError:
    import os
    os.system("pip install trello")
try:
    import rapidtables
except ImportError:
    import os
    os.system("pip install rapidtables")
import rapidtables
from commands import *
from trello import TrelloApi
import requests

__version__ = "0.0.6"

ENCRYPTED_TRELLO_API_TOKEN = [33, -20, -56, -18, -57, -57, -47, 48, 33, 31, -49, -14, -56, -55, -41, 0, -16, -20, -50,
                              -20, -59, -5, -44, 4, 29, -20, -48, -16, -54, -52, 1, 4, -13, 27, -49, -16, -55, -10, 0, 1,
                              -17, -19, -57, 29, -11, -51, -49, 50, 33, 31, -5, 28, -11, -58, 2, 3, 28, -23, -5, -15, -58,
                              -6, 3, 53]

ENCRYPTED_TRELLO_API_KEY = [-20, -21, -4, -22, -12, -10, -47, 3, 32, -23, -50, 31, -60, -55, 0, 52, -18, 28, -52, -20,
                            -61, -8, -43, 53, -19, -22, -55, -22, -61, -6, -45, 50]


def reset_password():
    password = Str.input_pass()
    GIV["api_password"] = password
    return password


try:
    password = GIV["api_password"]
    if "reset" in sys.argv:
        password = reset_password()
except (NameError, KeyError):
    password = reset_password()

TRELLO_API_TOKEN = Str.decrypt(ENCRYPTED_TRELLO_API_TOKEN, password)
TRELLO_API_KEY = Str.decrypt(ENCRYPTED_TRELLO_API_KEY, password)

WORKING_BOARD_NAME = "Tody"

trello = TrelloApi(TRELLO_API_KEY)

trello.set_token(TRELLO_API_TOKEN)

my_member_id = trello.tokens.get_member(TRELLO_API_TOKEN)["id"]

my_boards = requests.get(f'https://api.trello.com/1/members/me/boards?key={TRELLO_API_KEY}&token={TRELLO_API_TOKEN}').json()

for board in my_boards:
    if board["name"] == WORKING_BOARD_NAME:
        # print(board["name"], board["id"])
        board_id = board["id"]

board_info = requests.get(f'https://api.trello.com/1/boards/{board_id}?key={TRELLO_API_KEY}'
                          f'&token={TRELLO_API_TOKEN}').json()

# Print.prettify(board_info)

board_url_id = board_info['shortUrl'].split("/")[-1]

board_lists_url = f"https://api.trello.com/1/boards/{board_url_id}/?key={TRELLO_API_KEY}" \
                  f"&token={TRELLO_API_TOKEN}&lists=all"

board_lists = requests.get(board_lists_url).json()["lists"]

# Print.prettify(board_lists)

time = []

for list_ in board_lists:
    if not list_["closed"]:
        list_id = list_["id"]
        list_name = list_["name"]
        all_time = 0

        cards = requests.get(f"https://api.trello.com/1/lists/{list_id}/cards?key={TRELLO_API_KEY}"
                             f"&token={TRELLO_API_TOKEN}&fields=id,name,badges,labels").json()

        # Print.prettify(cards)
        for card in cards:
            card_id = card["id"]
            card_name = card["name"]
            # Print("       ", card_name, card_id)

            try:
                card_time = Str.substring(card_name, "(").strip().strip(")")
            except KeyError:
                card_time = ""
                Print.colored("           ", 'Add time!', card_name, "red", "on_black")
            while "(" in card_time:
                card_time = Str.substring(card_time, "(")
            # Print("           ", card_time)

            try:
                card_mins = Str.get_integers(card_time)[0]
                all_time += card_mins
            except IndexError:
                Print.colored("           ", "Add mins!", card_name, "red", "on_black")
            try:
                card_counts = Str.get_integers(card_time)[1]
            except IndexError:
                Print.colored("           ", "Add counts!", card_name, "red", "on_black")
        time.append({
            # "list_id": list_id,
            "list_name": list_name,
            "time": all_time})
        # Print("   ", list_name, list_id, f"\ttime: {all_time} mins")

header, rows = rapidtables.format_table(time, fmt=rapidtables.FORMAT_GENERATOR_COLS)
spacer = '  '
Print.colored(spacer.join(header), 'blue')
Print.colored('-' * sum([(len(x) + 2) for x in header]), 'grey')
for row in rows:
    print(spacer.join(row))
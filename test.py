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
from commands import *
from trello import TrelloApi

__version__ = "0.0.4"

ENCRYPTED_TRELLO_APP_KEY = [33, -20, -56, -18, -57, -57, -47, 48, 33, 31, -49, -14, -56, -55, -41, 0, -16, -20, -50,
                            -20, -59, -5, -44, 4, 29, -20, -48, -16, -54, -52, 1, 4, -13, 27, -49, -16, -55, -10, 0, 1,
                            -17, -19, -57, 29, -11, -51, -49, 50, 33, 31, -5, 28, -11, -58, 2, 3, 28, -23, -5, -15, -58,
                            -6, 3, 53]


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

TRELLO_APP_KEY = Str.decrypt(ENCRYPTED_TRELLO_APP_KEY, password)


trello = TrelloApi(TRELLO_APP_KEY)

print(type(trello), trello)

dirify(trello)
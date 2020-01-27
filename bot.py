#! python3
# -*- coding: utf-8 -*-
import os
import sys
try:
    from commands import *
except ImportError:
    os.system("python3 -m pip install git+https://github.com/egigoka/commands")
    from commands import *
try:
    import telegrame
except ImportError:
    os.system("python3 -m pip install git+https://github.com/egigoka/telegrame")
    import telegrame
try:
    import telebot
except ImportError:
    os.system("python3 -m pip install pytelegrambotapi")
    import telebot

__version__ = "0.0.11"

my_chat_id = 5328715

# change version
if OS.hostname == "MacBook-Pro-Mac.local":
    import re
    filepath = Path.safe__file__(__file__)
    content = File.read(filepath)
    lines = Str.nl(content)
    for cnt, line in enumerate(lines):
        if "__version__" in line:
            regexp = re.compile(r"(\d+)(?!.*\d)")
            last_ver = re.findall(r"(\d+)(?!.*\d)", line)
            replace = str(int(last_ver[0])+1)
            new = re.sub(r"(\d+)(?!.*\d)", replace, line)
            lines[cnt] = new
            break
    new_content = "\r\n".join(lines)
    File.write(filepath, new_content, mode="w")
# end changing version

# encryption part
encrypted_telegram_token = [-20, -23, -55, -19, -56, -54, -47, 4, -17, -16, -47, -6, -46, -37, -32, 49, 10, -15, -32,
                            -2, -25, -8, 15, 34, 46, -21, 4, -20, 2, -3, -49, 26, 43, 1, -35, -20, 5, -1, -29, 30, 16,
                            12, 11, 12, -2, -4]  # production


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

telegram_token = Str.decrypt(encrypted_telegram_token, password)
# end encryption part


def start_todoist_bot(none_stop=True):
    telegram_api = telebot.TeleBot(telegram_token, threaded=False)

    @telegram_api.message_handler(content_types=["text"])
    def reply_all_messages(message):
        # init vars
        chat_id = message.chat.id
        message_id = message.message_id
        try:
            print(chat_id, message_id, message.text)
        except:
            print(chat_id, message_id)

        main_markup = telebot.types.ReplyKeyboardMarkup()
        main_button = telebot.types.KeyboardButton('Upd!')
        main_markup.row(main_button)
        main_markup.row()

        out = "Access denied!"
        if chat_id == my_chat_id:
            out = "```"+newline+Console.get_output("python3", "test.py")+"```"
        print(out)
        telegram_api.send_message(chat_id, out, parse_mode="markdown", reply_markup=main_markup)


    telegram_api.polling(none_stop=none_stop)
    # https://github.com/eternnoir/pyTelegramBotAPI/issues/273


def main():
    telegrame.very_safe_start_bot(start_todoist_bot)


if __name__ == '__main__':
    main()

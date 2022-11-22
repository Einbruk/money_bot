"""
    This is a Telegram bot that allows you to keep track of money
    spent with your friends at a party and while co-living.
    Try /help command for info on how to use it.
    main.py handles commands for the bot.
"""

import telebot
import libs


with open("./data/config.txt", "r") as cfg:
    token = cfg.read()
help = "Supported commands:\n" \
       "/show - show balance\n" \
       "/split _who_ _amount_ _optional_ - new spending, who payed, amount," \
       " and to whom to spilt with (default = all added)\n" \
       "/add _name_ - add person to a group who spends together\n" \
       "/remove _name_ - remove a person from a group\n" \
       "/loan _who_ _amount_ _to_whom_ - when someone gave money to someone"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=["help"])
def helper(message) -> None:
    bot.send_message(message.chat.id, help)


@bot.message_handler(commands=["add"])
def add_person(message) -> None:
    command = message.text.split()
    try:
        if libs.user_addition(message.chat.id, command[1].lower()):
            bot.send_message(message.chat.id, "Юзер {name} добавлен в группу.".format(name=command[1].capitalize()))
        else:
            bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")
    except Exception:
        print(Exception.__name__)
        bot.send_message(message.chat.id, "Ошибка, возникло исключение, проверьте ввод.")


@bot.message_handler(commands=["show"])
def show_totals(message) -> None:
    try:
        display_text = libs.show(message.chat.id)
        bot.send_message(message.chat.id, display_text)
    except Exception:
        bot.send_message(message.chat.id, "Ошибка, возникло исключение, проверьте ввод.")


@bot.message_handler(commands=["remove"])
def remove(message) -> None:
    command = message.text.split()
    try:
        if libs.remove_user(message.chat.id, command[1].lower()):
            bot.send_message(message.chat.id, "Юзер {name} удалён.".format(name=command[1].capitalize()))
        else:
            bot.send_message(message.chat.id, "Возникла непредвиденная ошибка.")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка, возникло исключение, проверьте ввод.")


@bot.message_handler(commands=["split"])
def split(message) -> None:
    command = message.text.split()
    try:
        for ind in range(3, len(command)):
            command[ind] = command[ind].lower()
        if libs.split_costs(message.chat.id, command[1].lower(), int(command[2]), command[3:]):
            bot.send_message(message.chat.id, "Трата успешно добавлена.")
        else:
            bot.send_message(message.chat.id, "Ошибка, проверьте ввод.")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка, возникло исключение, проверьте ввод.")


@bot.message_handler(commands=["loan"])
def loan(message) -> None:
    command = message.text.split()
    try:
        if libs.loan(message.chat.id, command[1].lower(), int(command[2]), command[3].lower()):
            bot.send_message(message.chat.id, "Ок")
        else:
            bot.send_message(message.chat.id, "Ошибка, проверьте ввод.")
    except Exception:
        bot.send_message(message.chat.id, "Ошибка, возникло исключение, проверьте ввод.")


bot.polling(none_stop=True)

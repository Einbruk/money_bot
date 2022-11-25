"""
    This is additional file for py_money_bot
    It handles user data and calculations
    All data stored as json object in a chats.json
"""

import json
import bot_logging


@bot_logging.log_decorator
def read_json() -> dict:
    """
    Since json object does not support integer for a key? this function reads a json file where
    all of user data is stored and returnes a dictionary with integer keys to process this data
    :return: dict - a dictionary with user data
    """
    with open("./data/user_data.json", "r", encoding="utf-8") as user_data:
        balance = json.load(user_data)
    li_o =[]
    for key in balance.keys():
        li_o.append(key)

    for key in li_o:
        li = []
        balance[int(key)] = balance.pop(key)

        for in_key in balance[int(key)].keys():
            if isinstance(in_key, str):
                if in_key.isnumeric():
                    li.append(in_key)

        for li_key in li:
            balance[int(key)][int(li_key)] = balance[int(key)].pop(li_key)

    return balance


@bot_logging.log_decorator
def user_addition(chat_id: int, new_name: str, prio: int) -> bool:
    """
    This function adds new user to a specific chat if chat_id  not in dictionary, it adds it as well
    :param new_name: str - username to add
    :param chat_id: int - id of a chat
    :param prio: int - priority of user to split
    :return: bool - function returns true if operation was successful if any errors returns false
    """

    balance = read_json()
    if prio is None:
        prio = 1
    if chat_id not in balance.keys():
        balance[chat_id] = {}
        balance[chat_id]["count"] = 0

    num_of_users = balance[chat_id]["count"]
    all_names = [balance[chat_id][index][0] for index in range(num_of_users)]
    new_name = str(prio) + " " + new_name

    if new_name in all_names:
        bot_logging.log("Name already exists")
        return False
    else:
        balance[chat_id]["count"] += 1
        for u_id in range(num_of_users):
            balance[chat_id][u_id].append(0)

        balance[chat_id][num_of_users] = [new_name]
        for index in range(num_of_users):
            balance[chat_id][num_of_users].append(0)
        balance[chat_id][num_of_users].append(None)

    with open("./data/user_data.json", "w", encoding="utf-8") as user_data:
        json.dump(balance, user_data, indent=4)
    return True


@bot_logging.log_decorator
def show(chat_id: int) -> str:
    """
    Function to sum up who owes who
    :param chat_id: int - an id number of a chat
    :return: str - a text of how much money each user owes to others
    """
    balance = read_json()

    text_to_print = ""
    num_of_users = balance[chat_id]["count"]
    if num_of_users >= 2:
        for u_id in range(num_of_users):
            text_to_print += "{user} ({prio}):\n".format(user=balance[chat_id][u_id][0][2:].capitalize(),
                                                         prio=balance[chat_id][u_id][0][:1])
            for index in range(1, num_of_users + 1):
                if u_id + 1 != index:
                    text_to_print += "\towes {name}: {amount}\n".format(name=balance[chat_id][index - 1][0][2:].capitalize(),
                                                                        amount=balance[chat_id][u_id][index])
    else:
        text_to_print = "Less than two users"
    return text_to_print


@bot_logging.log_decorator
def remove_user(chat_id: int, r_name: str) -> bool:
    """
    This function removes a user from splitting costs, it can not
    remove user whose balance is not zero
    :param chat_id: int - an id number for a chat
    :param r_name: str - name of a user to be removed
    :return: bool - returns True if removed successfully
    """
    balance = read_json()

    if chat_id not in balance.keys():
        bot_logging.log("chat is not in the list")
        return False

    num_of_users = balance[chat_id]["count"]
    all_names = [balance[chat_id][index][0][2:] for index in range(num_of_users)]

    if r_name not in all_names:
        bot_logging.log("user does not exists")
        return False
    else:
        for u_id in range(num_of_users):
            if balance[chat_id][u_id][0][2:] == r_name:
                r_name_id = u_id
                for index in range(1, num_of_users + 1):
                    if balance[chat_id][u_id][index] != 0 and balance[chat_id][u_id][index] is not None:
                        bot_logging.log("User {user} owes {amount} to {name}".format(user=balance[chat_id][u_id][0],
                                                                            amount=balance[chat_id][u_id][index],
                                                                            name=balance[chat_id][index - 1][0]))
                        return False

    for user in range(num_of_users):
        balance[chat_id][user].pop(r_name_id + 1)
    balance[chat_id]["count"] -= 1
    balance[chat_id].pop(r_name_id)
    for user in range(r_name_id, num_of_users - 1):
        balance[chat_id][user] = balance[chat_id].pop(user + 1)

    with open("./data/user_data.json", "w", encoding="utf-8") as user_data:
        json.dump(balance, user_data, indent=4)
    return True


@bot_logging.log_decorator
def split_costs(chat_id: int, who_payed: str, amount: int, to_split: list = None) -> bool:
    """
    This function calculates how much who owes whom
    :param chat_id: int - id number of a chat
    :param who_payed: str - name of person who payed
    :param amount: int - amount payed
    :param to_split: list - list of people to split with if empty splits for all
    :return:
    """
    balance = read_json()

    num_of_users = balance[chat_id]["count"]
    all_names = [balance[chat_id][index][0][2:] for index in range(num_of_users)]

    if who_payed not in all_names:
        bot_logging.log("Error, User not found")
        bot_logging.log(str(all_names))
        return False
    for name in to_split:
        if name not in all_names:
            bot_logging.log("Err, user not found")
            bot_logging.log(str(all_names))
            return False

    if len(to_split) != 0:
        split = int(amount / (len(to_split) + 1))
    else:
        all_count = 0
        for u_id in range(num_of_users):
            all_count += int(balance[chat_id][u_id][0][:1])
        print(all_count)
        split = int(amount / all_count)

    for u_id in range(num_of_users):
        if balance[chat_id][u_id][0][2:] == who_payed:
            who_payed_id = u_id
            break

    if len(to_split) != 0:
        for u_id in range(num_of_users):
            if balance[chat_id][u_id][0][2:] in to_split:
                balance[chat_id][u_id][who_payed_id + 1] += split
                balance[chat_id][who_payed_id][u_id + 1] -= split
    else:
        for u_id in range(num_of_users):
            if who_payed_id != u_id:
                balance[chat_id][u_id][who_payed_id + 1] += split * int(balance[chat_id][u_id][0][:1])
                balance[chat_id][who_payed_id][u_id + 1] -= split * int(balance[chat_id][u_id][0][:1])

    with open("./data/user_data.json", "w", encoding="utf-8") as user_data:
        json.dump(balance, user_data, indent=4)
    return True


@bot_logging.log_decorator
def loan(chat_id: int, who_gave: str, amount: int, who_recieved: str) -> bool:
    """
    This function allows to loan money between users
    :param chat_id: int - id number of a given chat
    :param who_gave: str - username of one who loaned money
    :param amount: int - amount of money loaned
    :param who_recieved: str - username of one who took money
    :return: bool - true if function completed successfully
    """
    balance = read_json()

    num_of_users = balance[chat_id]["count"]
    all_names = [balance[chat_id][index][0][2:] for index in range(num_of_users)]
    if who_gave not in all_names or who_recieved not in all_names:
        bot_logging.log("User not found")
        return False

    for u_id in range(num_of_users):
        if balance[chat_id][u_id][0][2:] == who_gave:
            who_gave_id = u_id
            break

    for u_id in range(num_of_users):
        if balance[chat_id][u_id][0][2:] == who_recieved:
            balance[chat_id][u_id][who_gave_id + 1] += amount
            balance[chat_id][who_gave_id][u_id + 1] -= amount
            break

    with open("./data/user_data.json", "w", encoding="utf-8") as user_data:
        json.dump(balance, user_data, indent=4)
    return True



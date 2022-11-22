"""
 This is additional file for py_money_bot
It handles logging decorator and logging functionality
"""

import datetime
import functools


def log(message: str) -> None:
    with open("./data/money_bot.log", "a", encoding="utf-8") as log_file:
        time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        message = time + "  ---  " + message + "\n"
        log_file.write(message)


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        log("Function {fname} called with arguments {arg}, {kwarg}".format(fname=func.__name__,
                                                                           arg=repr(args), kwarg=repr(kwargs)))
        value = func(*args, **kwargs)
        if func.__name__ != "show" and func.__name__ != "read_json":
            log("Function returned: {}".format(value))
        return value
    return wrapper


from telebot.handler_backends import State, StatesGroup


class States(StatesGroup):
    EDIT_NAME = State()
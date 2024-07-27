from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from utils.game.helpers_lobby import *
from utils.users.helpers import *


def manage_lobby_keyboard():
    keyboard = quick_markup({
        "Начать игру": {"callback_data": "start_game"},
        "Список игроков": {"callback_data": "list_players_lobby"},
        "Удалить лобби": {"callback_data": "delete_lobby"}
    }, row_width = 1)
    return keyboard


def list_players_keyboard(chat_id: int):
    keyboard = InlineKeyboardMarkup()
    for user_id in get_list_players_lobby(chat_id):
        user_name = get_info_about_user(user_id).name
        keyboard.add(InlineKeyboardButton(f"{user_name}{" ⭐️" if is_creator(user_id, chat_id) else ""}",
                                          callback_data=f"confirmkick_{user_id}"))
    keyboard.add(InlineKeyboardButton("Назад ↩️", callback_data="back_to_manage_lobby"))
    return keyboard


def kick_keyboard(user_id: int):
    keyboard = quick_markup({
        "Исключить": {"callback_data": f"kick_{user_id}"}, "Назад ↩️": {"callback_data": "back_to_list_players"}
    }, row_width = 2)
    return keyboard
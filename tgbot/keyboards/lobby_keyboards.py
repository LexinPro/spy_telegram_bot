from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from utils.lobby_manager import *
from utils.users_data import *


def manage_lobby_keyboard():
    keyboard = quick_markup({
        "Начать игру": {"callback_data": "start_game"},
        "Список игроков": {"callback_data": "list_players_lobby"},
        "Удалить лобби": {"callback_data": "delete_lobby"}
    }, row_width = 1)
    return keyboard


def list_players_keyboard(lobby_id: int):
    keyboard = InlineKeyboardMarkup()
    lobby = find_lobby(lobby_id)
    for player_id in lobby.get_list_players():
        player_name = find_user(player_id).name
        keyboard.add(InlineKeyboardButton(f"{player_name}{" ⭐️" if player_id == lobby.creator_id else ""}",
                                          callback_data=f"confirmkick_{player_id}"))
    keyboard.add(InlineKeyboardButton("Назад ↩️", callback_data="back_manage_lobby"))
    return keyboard


def kick_keyboard(user_id: int):
    keyboard = quick_markup({
        "Исключить": {"callback_data": f"kick_{user_id}"}, "Назад ↩️": {"callback_data": "back_list_players"}
    }, row_width = 2)
    return keyboard
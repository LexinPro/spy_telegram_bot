from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from utils.lobby_manager import *
from utils.users_data import *


def select_members_keyboard(lobby_id: int):
    keyboard = InlineKeyboardMarkup()
    lobby = find_lobby(lobby_id)
    for player_id in lobby.get_list_players():
        if player_id != lobby.leaders[-1]:
            player_name = find_user(player_id).name
            if player_id not in lobby.get_list_members_of_robbery():
                keyboard.add(InlineKeyboardButton(f"{player_name}", callback_data=f"take_{player_id}"))
            else:
                keyboard.add(InlineKeyboardButton(f"{player_name} ✅", callback_data=f"donttake_{player_id}"))
    if lobby.count_members == lobby.max_count_members:
        keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="accept"))
    return keyboard


def manage_game_keyboard():
    keyboard = quick_markup({
        "Список игроков": {"callback_data": "list_players_lobby"},
        "Закончить игру": {"callback_data": "finish_game"}
    }, row_width=1)
    return keyboard


def show_role_keyboard():
    keyboard = quick_markup({
        "Показать роль": {"callback_data": "show_role"}
    })
    return keyboard


def hide_role_keyboard():
    keyboard = quick_markup({
        "Скрыть роль": {"callback_data": "hide_role"}
    })
    return keyboard


def choice_keyboard():
    keyboard = quick_markup({
        "⬜️": {"callback_data": "choice_true"},
        "⬛️": {"callback_data": "choice_false"}
    }, row_width=2)
    return keyboard

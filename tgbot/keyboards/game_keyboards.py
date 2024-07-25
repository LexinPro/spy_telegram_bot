from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from utils.game.helpers_lobby import *
from utils.game.helpers_game import *
from utils.users.helpers import *


def list_members_lobby_keyboard(chat_id: int):
    keyboard = InlineKeyboardMarkup()
    leader_id = get_leader_id(chat_id)
    for player_id in get_list_players_lobby(chat_id):
        if player_id != leader_id:
            player_name= get_info_about_user(player_id).name
            if not is_member(player_id, chat_id):
                keyboard.add(InlineKeyboardButton(f"{player_name}", callback_data=f"take_{chat_id}_{player_id}"))
            else:
                keyboard.add(InlineKeyboardButton(f"{player_name} ✅", callback_data=f"dont_take_{chat_id}_{player_id}"))
    if get_current_count_members_lobby(chat_id) == get_count_members_lobby(chat_id):
        keyboard.add(InlineKeyboardButton("Подтвердить", callback_data="accept"))
    return keyboard


def finish_game_keyboard(chat_id: int):
    keyboard = quick_markup({
        "Закончить игру": {"callback_data": "finish_game"}
    })
    return keyboard


def choice_keyboard():
    keyboard = quick_markup({
        "⬜️": {"callback_data": "choice_true"},
        "⬛️": {"callback_data": "choice_false"}
    }, row_width=2)
    return keyboard

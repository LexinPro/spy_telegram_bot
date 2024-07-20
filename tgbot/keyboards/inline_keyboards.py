from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.util import quick_markup

from utils.helpers import check_admin_lobby, list_players
from utils.users import get_info_user
from utils.models import Lobby


def info_command_keyboard():
    keyboard = quick_markup({
        "Изменить имя": {"callback_data": "edit_name"},
        "Установить пол": {"callback_data": "edit_sex"}
    }, row_width = 1)
    return keyboard


def choice_sex_keyboard():
    keyboard = quick_markup({
        "🚹 Мужской": {"callback_data": "edit_sex_m"}, "🚺 Женский": {"callback_data": "edit_sex_w"},
        "Назад": {"callback_data": "back_to_info_command"}
    }, row_width = 2)
    return keyboard


def manage_lobby_keyboard():
    keyboard = quick_markup({
        "Начать игру": {"callback_data": "start_game"},
        "Список игроков": {"callback_data": "list_players_lobby"}
    }, row_width = 1)
    return keyboard


def list_players_keyboard(chat_id: int):
    keyboard = InlineKeyboardMarkup()
    for user_id in list_players(chat_id):
        user_name = get_info_user(user_id)['NAME']
        keyboard.add(InlineKeyboardButton(f"{user_name}{" ⭐️" if check_admin_lobby(user_id, chat_id) else ""}",
                                          callback_data=f"kick_{chat_id}_{user_id}"))
    keyboard.add(InlineKeyboardButton("Назад", callback_data="back_to_manage_lobby"))
    return keyboard


def kick_confirm_keyboard(chat_id: int, user_id: int):
    keyboard = quick_markup({
        "Исключить": {"callback_data": f"confirm_{chat_id}_{user_id}"}, "Назад": {"callback_data": "back_to_list_players"}
    }, row_width = 2)
    return keyboard


def list_members_lobby_keyboards(lobby: Lobby):
    chat_id = lobby.chat_id
    leader_id = lobby.game.leaders[-1]
    keyboard = InlineKeyboardMarkup()
    for user_id in list_players(chat_id):
        if user_id != leader_id:
            user_name = get_info_user(user_id)['NAME']
            keyboard.add(InlineKeyboardButton(f"{user_name}{" ✅" if user_id in lobby.game.round.members else ""}",
                                              callback_data=f"take_{chat_id}_{user_id}"))
    keyboard.add(InlineKeyboardButton("Назад", callback_data="back_to_manage_lobby"))
    return keyboard


def back_keyboard(path: str):
    keyboard = quick_markup({
        "Назад": {"callback_data": f"back_to_{path}"}
    }, row_width = 1)
    return keyboard
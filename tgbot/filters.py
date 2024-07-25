from telebot.types import CallbackQuery
from utils.game.helpers_lobby import is_creator

# TODO: сделать несколько фильтров для коллбэков


def list_players_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data == "list_players_lobby" and is_creator(callback.from_user.id)


def kick_confirm_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "confirmkick" and is_creator(callback.from_user.id)


def kick_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "confirm" and is_creator(callback.from_user.id)

def back_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data in ("back_to_manage_lobby", "back_to_list_players") and is_creator(callback.from_user.id)


def delete_message_lobby_callback_filter(callback: CallbackQuery) -> bool:
    return ((callback.data == "list_players_lobby") or ("kick" in callback.data) or ("confirm" in callback.data)
             or (callback.data in ("back_to_manage_lobby", "back_to_list_players")))


def take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "take" and is_creator(callback.from_user.id)

def dont_take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    words = callback.data.split('_')
    if len(words) == 4:
        first_word, second_word = words[:2]
        return first_word == "dont" and second_word == "take" and is_creator(callback.from_user.id)
    else:
        return False
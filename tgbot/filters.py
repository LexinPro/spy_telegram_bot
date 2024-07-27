from telebot.types import CallbackQuery
from utils.game.helpers_lobby import *
from utils.game.helpers_game import *

# TODO: сделать несколько фильтров для коллбэков


def list_players_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data == "list_players_lobby" and is_creator(callback.from_user.id)


def kick_confirm_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "confirmkick" and is_creator(callback.from_user.id)


def kick_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "kick" and is_creator(callback.from_user.id)


def back_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data in ("back_to_manage_lobby", "back_to_list_players") and is_creator(callback.from_user.id)


def delete_lobby_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data == "delete_lobby" and is_creator(callback.from_user.id)


def delete_message_lobby_callback_filter(callback: CallbackQuery) -> bool:
    return ((callback.data == "list_players_lobby") or ("kick" in callback.data) or ("confirm" in callback.data)
             or (callback.data in ("back_to_manage_lobby", "back_to_list_players")) or 
             (callback.data == "delete_lobby"))


def take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    if len(callback.data.split('_')) == 3:
        first_word = callback.data.split('_')[0]
        chat_id = int(callback.data.split('_')[1])
        return first_word == "take" and is_leader(callback.from_user.id, chat_id)
    else:
        return False

def dont_take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    words = callback.data.split('_')
    if len(words) == 4:
        first_word, second_word = words[:2]
        chat_id = int(callback.data.split('_')[2])
        return first_word == "dont" and second_word == "take" and is_leader(callback.from_user.id, chat_id)
    else:
        return False
    

def start_game_callback_filter(callback: CallbackQuery) -> bool:
    creator_id = callback.from_user.id
    chat_id = get_chat_id_of_lobby(creator_id)
    return callback.data == "start_game" and is_creator(creator_id, chat_id)


def finish_game_callback_filter(callback: CallbackQuery) -> bool:
    creator_id = callback.from_user.id
    chat_id = get_chat_id_of_lobby(creator_id)
    return callback.data == "finish_game" and is_creator(creator_id, chat_id)

from telebot.types import Message, CallbackQuery

from utils.lobby_manager import *
from utils.users_data import *


def list_players_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data == "list_players_lobby" and is_creator_of_lobby(callback.from_user.id)


def kick_confirm_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "confirmkick" and is_creator_of_lobby(callback.from_user.id)


def kick_callback_filter(callback: CallbackQuery) -> bool:
    first_word = callback.data.split('_')[0]
    return first_word == "kick" and is_creator_of_lobby(callback.from_user.id)


def back_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data in ("back_manage_lobby", "back_list_players") and is_creator_of_lobby(callback.from_user.id)


def delete_lobby_callback_filter(callback: CallbackQuery) -> bool:
    return callback.data == "delete_lobby" and is_creator_of_lobby(callback.from_user.id)


def delete_message_lobby_callback_filter(callback: CallbackQuery) -> bool:
    return ((callback.data == "list_players_lobby") or ("kick" in callback.data) or ("confirm" in callback.data)
             or (callback.data in ("back_to_manage_lobby", "back_to_list_players")) or 
             (callback.data == "delete_lobby"))


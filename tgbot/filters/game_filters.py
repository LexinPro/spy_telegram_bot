from telebot.types import CallbackQuery
from utils.lobby_manager import *
from utils.users_data import *


def start_game_callback_filter(callback: CallbackQuery) -> bool:
    creator_id = callback.from_user.id
    lobby = fetch_lobby(creator_id)
    return callback.data == "start_game" and lobby != None and creator_id == lobby.creator_id


def take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    leader_id = callback.from_user.id
    lobby = fetch_lobby(leader_id)
    words = callback.data.split('_')
    if len(words) == 2 and lobby != None:
        first_word = words[0]
        return first_word == "take" and leader_id == lobby.leaders[-1] and not lobby.status_round
    else:
        return False


def dont_take_player_on_robbery_callback_filter(callback: CallbackQuery) -> bool:
    leader_id = callback.from_user.id
    lobby = fetch_lobby(leader_id)
    words = callback.data.split('_')
    if len(words) == 2 and lobby != None:
        first_word = words[0]
        return first_word == "donttake" and leader_id == lobby.leaders[-1] and not lobby.status_round
    else:
        return False
    

def accept_callback_filter(callback: CallbackQuery) -> bool:
    leader_id = callback.from_user.id
    lobby = fetch_lobby(leader_id)
    words = callback.data.split('_')
    if len(words) == 1 and lobby != None and lobby.leaders != None and lobby.count_members != None and lobby.max_count_members != None:
        first_word = words[0]
        return first_word == "accept" and leader_id == lobby.leaders[-1] and not lobby.status_round and lobby.count_members == lobby.max_count_members
    else:
        return False
    

def show_role_callback_filter(callback: CallbackQuery) -> bool:
    leader_id = callback.from_user.id
    lobby = fetch_lobby(leader_id)
    words = callback.data.split('_')
    if len(words) == 2 and lobby != None and lobby.status_game:
        first_word = words[0]
        second_word = words[1]
        return first_word == "show" and second_word == "role"
    else:
        return False


def hide_role_callback_filter(callback: CallbackQuery) -> bool:
    leader_id = callback.from_user.id
    lobby = fetch_lobby(leader_id)
    words = callback.data.split('_')
    if len(words) == 2 and lobby != None and lobby.status_game:
        first_word = words[0]
        second_word = words[1]
        return first_word == "hide" and second_word == "role"
    else:
        return False
    

def choice_callback_filter(callback: CallbackQuery) -> bool:
    member_id = callback.from_user.id
    lobby = fetch_lobby(member_id)
    words = callback.data.split('_')
    if len(words) == 2 and lobby != None:
        first_word = words[0]
        return first_word == "choice" and member_id in lobby.get_list_members_of_robbery() and lobby.status_round
    else:
        return False
    

def finish_game_callback_filter(callback: CallbackQuery) -> bool:
    creator_id = callback.from_user.id
    return callback.data == "finish_game" and is_creator_of_lobby(creator_id)

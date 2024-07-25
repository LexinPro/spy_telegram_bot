from utils.game.models import *


def create_lobby(creator_id: int, chat_id: int):
    lobbies_dict[chat_id] = Lobby(chat_id, creator_id)
    players_dict[creator_id] = chat_id


def delete_lobby(chat_id: int):
    for player_id in list(lobbies_dict[chat_id].players.keys()):
        players_dict.pop(player_id)
    lobbies_dict.pop(chat_id)


def join_to_lobby(player_id: int, chat_id: int):
    lobbies_dict[chat_id].players[player_id] = None
    lobbies_dict[chat_id].count_players += 1
    players_dict[player_id] = chat_id


def remove_from_lobby(player_id: int, chat_id: int):
    players_dict.pop(player_id)
    lobbies_dict[chat_id].count_players -= 1
    lobbies_dict[chat_id].players.pop(player_id)


def is_player_in_lobby(player_id: int, chat_id: int = 0) -> bool:
    if chat_id == 0:
        return player_id in players_dict
    if player_id not in players_dict:
        return False
    return chat_id == players_dict[player_id]


def is_creator(player_id: int, chat_id: int = 0) -> bool:
    if chat_id == 0:
        for lobby in list(lobbies_dict.values()):
            if lobby.creator_id == player_id:
                return True
        return False
    return lobbies_dict[chat_id].creator_id == player_id


def is_lobby_exist(chat_id: int) -> bool:
    return chat_id in lobbies_dict


def is_lobby_play(chat_id: int) -> bool:
    return lobbies_dict[chat_id].status


def get_chat_id_of_lobby(player_id: int) -> int:
    return players_dict[player_id]


def get_count_players_lobby(chat_id: int) -> int:
    return lobbies_dict[chat_id].count_players


def get_list_players_lobby(chat_id: int) -> list[int]:
    return list(lobbies_dict[chat_id].players.keys())

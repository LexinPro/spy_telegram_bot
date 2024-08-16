from utils.models import Lobby, lobbies, UserOfTelegramBot, users
from utils.users_data import find_user


def create_lobby(creator_id: int, lobby_id: int):
    lobbies.append(Lobby(lobby_id, creator_id))
    user = find_user(creator_id)
    user.join_to_lobby(lobby_id)


def delete_lobby(lobby_id: int):
    lobby = find_lobby(lobby_id)
    for player_id in list(lobby.players.keys()):
        player = find_user(player_id)
        player.leave_from_lobby()
    lobbies.remove(lobby)


def check_lobby_exists(lobby_id: int) -> bool:
    for lobby in lobbies:
        if lobby.id == lobby_id:
            return True
    return False


def find_lobby(lobby_id: int) -> Lobby:
    for lobby in lobbies:
        if lobby.id == lobby_id:
            return lobby


def fetch_lobby(user_id: int) -> Lobby:
    user = find_user(user_id)
    return find_lobby(user.lobby_id)


def is_creator_of_lobby(user_id: int) -> bool:
    lobby = fetch_lobby(user_id)
    if lobby is None:
        return False
    return lobby.creator_id == user_id

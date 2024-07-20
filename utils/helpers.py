from utils.models import Lobby

def new_lobby(admin_id: int, chat_id: int):
    LOBBIES[chat_id] = Lobby(admin_id, chat_id)
    PLAYERS[admin_id] = chat_id

def check_lobby(chat_id: int) -> bool:
    return chat_id in LOBBIES

def check_player(player_id: int) -> bool:
    return player_id in PLAYERS

def check_player_lobby(player_id: int, chat_id: int) -> bool:
    if player_id in PLAYERS:
        return chat_id == PLAYERS[player_id]
    return False

def check_admin_lobby(player_id: int, chat_id: int = -1) -> bool:
    if chat_id == -1:
        chat_id = get_chat_id(player_id)
    if chat_id == -1:
        return False
    return player_id == LOBBIES[chat_id].admin_id

def join(player_id: int, chat_id: int):
    LOBBIES[chat_id].player_join(player_id)
    PLAYERS[player_id] = chat_id

def remove(player_id: int) -> int:
    chat_id = PLAYERS[player_id]

    if LOBBIES[chat_id].admin_id == player_id:
        # *Удаляем из PLAYERS всех игроков, затем возвращаем удалённое лобби из LOBBIES
        for id in list(LOBBIES[chat_id].players.keys()):
            PLAYERS.pop(id)
        return LOBBIES.pop(chat_id)
    
    else:
        LOBBIES[chat_id].player_remove(player_id)
        PLAYERS.pop(player_id)
        return chat_id
    
def count_players(chat_id: int) -> bool:
    return LOBBIES[chat_id].count_players

def list_players(chat_id: int) -> list[int]:
    return list(LOBBIES[chat_id].players.keys())

def get_chat_id(player_id: int) -> int:
    if player_id in PLAYERS:
        return PLAYERS[player_id]
    return -1

def start(chat_id: int):
    lobby = LOBBIES[chat_id]
    lobby.start_game()
    return lobby


LOBBIES = dict()
PLAYERS = dict()

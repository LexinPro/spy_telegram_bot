from utils.game.models import *
from random import shuffle


def start_game(chat_id: int):
    lobbies_dict[chat_id].start_game()


def start_new_round(chat_id: int):
    lobbies_dict[chat_id].start_new_round()


def get_count_members_lobby(chat_id: int) -> int:
    return lobbies_dict[chat_id].count_members


def get_current_count_members_lobby(chat_id: int):
    return len(lobbies_dict[chat_id].members)


def get_players_and_roles(chat_id: int) -> dict[int, str]:
    return lobbies_dict[chat_id].players


def get_leader_id(chat_id: int) -> int:
    return lobbies_dict[chat_id].leaders[-1]


def get_together_score(chat_id: int) -> str:
    return lobbies_dict[chat_id].score["together"]


def add_member(player_id: int, chat_id: int):
    lobbies_dict[chat_id].members[player_id] = None


def remove_member(player_id: int, chat_id: int):
    lobbies_dict[chat_id].members.pop(player_id)


def is_member(player_id: int, chat_id: int) -> bool:
    return player_id in lobbies_dict[chat_id].members


def get_list_members_lobby(chat_id: int) -> list[int]:
    return list(lobbies_dict[chat_id].members.keys())


def vote(player_id: int, chat_id: int, choice: bool):
    lobbies_dict[chat_id].members[player_id] = choice


def check_everyone_voted(chat_id: int) -> bool:
    for choice in get_choices_of_members(chat_id):
        if choice == None:
            return False
    return True


def get_choices_of_members(chat_id: int) -> bool:
    return shuffle(list(lobbies_dict[chat_id].members.values()))


def sum_up_of_round(chat_id: int):
    lobby = lobbies_dict[chat_id]
    result = all(list(lobby.members.values()))
    if result:
        lobby.score["robbers"] += 1
        lobby.score["together"][lobby.round_number - 1] = "⬜️"
    else:
        lobby.score["spies"] += 1
        lobby.score["together"][lobby.round_number - 1] = "⬛️"


def check_end_game(chat_id: int) -> bool:
    lobby = lobbies_dict[chat_id]
    if lobby.round_number >= 6 or lobby.score["robbers"] >= 3 or lobby.score["spies"] >= 3:
        return True
    return False

def get_team_winner(chat_id: int) -> bool:
    lobby = lobbies_dict[chat_id]
    if lobby.score["robbers"] >= 3:
        return "robbers"
    else:
        return "spies"


def finish_game(chat_id: int):
    lobbies_dict[chat_id].finish_game()


def get_round_number(chat_id: int):
    return lobbies_dict[chat_id].round_number
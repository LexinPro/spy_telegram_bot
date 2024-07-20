from random import choice

from utils.settings_lobby import settings_lobby


"""
Lobby
|-> chat_id
|-> admin_id
|-> count_players
|-> players (dict)
?   |-> 103: Robber
?   |-> 104: Spy
?   |-> 105: None
?   |-> 106
?   |-> 107
|-> status (bool)
|-> game (class)
    |-> count_players
    |-> count_spies
    |-> spies
    |-> score (dict)
        |-> robbers
        |-> spies
        |-> together
    |-> leaders (list)
    |-> num_round
    |-> round (class)
        |-> count_members
        |-> members
?           |-> 103: True
?           |-> 104: False
?           |-> 107: None
"""


class Lobby:
    def __init__(self, admin_id: int, chat_id: int):
        self.chat_id = chat_id
        self.admin_id = admin_id
        self.count_players = 1
        self.players = {
            admin_id: None
        }
        self.status = False
        self.game = None
    

    def start_game(self):
        self.game = Game(self.count_players)

        for player_id in self.players.keys():
            self.players[player_id] = "Robber"
        k = 0
        while k < self.game.count_spies:
            random_player_id = choice(list(self.players.keys()))
            if self.players[random_player_id] != "Spy":
                self.players[random_player_id] = "Spy"
                k += 1
        
        self.status = True
        self.game.start_round(self.players)

    
    def player_join(self, player_id):
        self.players[player_id] = None
        self.count_players += 1

    def player_remove(self, player_id):
        self.players.pop(player_id)
        self.count_players -= 1



class Game:
    def __init__(self, count_players: int):
        self.count_players = count_players
        self.count_spies = settings_lobby[count_players]["count_spies"]
        
        self.score = {
            'robbers': 0,
            'spies': 0,
            'together': "1⃣2⃣3⃣4⃣5⃣"
        }

        self.round = None
        self.num_round = 0
        self.leaders = []

    def start_round(self, players: dict):
        self.num_round += 1
        self.round = Round(self.num_round, self.count_players)
        leader = choice(list(players.keys()))
        while leader in self.leaders:
            leader = choice(list(players.keys()))
        self.leaders.append(leader)


class Round:
    def __init__(self, num_round: int, count_players: int):
        self.count_members = settings_lobby[count_players]["count_go_to_robbery"][num_round]
        self.members = dict()
    
    def add_member(self, player_id: int):
        self.members[player_id] = None
    
    def member_vote(self, player_id: int, vote: bool):
        self.members[player_id] = vote
    
    def check_all_vote(self) -> bool:
        return all(vote != None for vote in self.members.values)

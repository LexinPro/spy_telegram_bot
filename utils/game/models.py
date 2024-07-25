from random import choice

from utils.game.settings_lobby import settings_lobby


players_dict = dict()
lobbies_dict = dict()


class Lobby:
    def __init__(self, chat_id: int, creator_id: int):
        self.chat_id = chat_id
        self.creator_id = creator_id
        self.players = {
            creator_id: None,
        }
        self.count_players = 1
        self.count_spies = None
        self.status = False
        self.score = {
            "robbers": None,
            "spies": None,
            "together": None
        }
        self.leaders = None
        self.round_number = None
        self.count_members = None
        self.members = None


    def start_game(self):
        self.count_spies = settings_lobby[self.count_players]["count_spies"]
        self.assign_roles()
        self.set_up_score()
        self.round_number = 0
        self.status = True
        self.leaders = []


    def start_new_round(self):
        self.round_number += 1
        self.select_leader()
        self.count_members = settings_lobby[self.count_players]["count_members"][self.round_number - 1]
        self.members = {self.leaders[-1]: None}


    def finish_game(self):
        for player_id in list(self.players.keys()):
            self.players[player_id] = None
        self.count_spies = None
        self.status = False
        self.score = {
            "robbers": None,
            "spies": None,
            "together": None
        }
        self.leaders = None
        self.round_number = None
        self.count_members = None
        self.members = None


    def assign_roles(self):
        for player_id in list(self.players.keys()):
            self.players[player_id] = "robber"
        
        k = 0
        while k < self.count_spies:
            random_player_id = self.select_random_player_id()
            if self.players[random_player_id] == "robber":
                self.players[random_player_id] = "spy"
                k += 1

    def set_up_score(self):
        self.score["robbers"] = 0
        self.score["spies"] = 0
        self.score["together"] = "1⃣2⃣3⃣4⃣5⃣"


    def select_leader(self):
        random_player_id = self.select_random_player_id()
        while random_player_id in self.leaders:
            random_player_id = self.select_random_player_id()
        self.leaders.append(random_player_id)


    def select_random_player_id(self) -> int:
        return choice(list(self.players.keys()))
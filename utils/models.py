from random import choice, shuffle

from utils.settings_lobby import settings_lobby


users = list()
lobbies = list()


class UserOfTelegramBot:
    def __init__(self, id, name, gender="Не указан"):
        self.id = id
        self.name = name
        self.gender = gender
        self.is_playing = False
        self.lobby_id = None

    def __str__(self):
        return f"{self.id};{self.name};{self.gender};\n"

    def update_name(self, new_name):
        self.name = new_name

    def update_gender(self, new_gender):
        self.gender = new_gender

    def join_to_lobby(self, lobby_id: int):
        self.is_playing = True
        self.lobby_id = lobby_id

    def leave_from_lobby(self):
        self.is_playing = False
        self.lobby_id = None



class Lobby:
    def __init__(self, chat_id: int, creator_id: int):
        self.id = chat_id
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
        self.max_count_members = None
        self.members = None


    def add_player(self, user_id: int):
        self.players[user_id] = None
        self.count_players += 1

    
    def remove_player(self, user_id: int):
        self.players[user_id] = None
        self.count_players -= 1


    def start_game(self):
        self.count_spies = settings_lobby[self.count_players]["count_spies"]
        self.assign_roles()
        self.reset_score()
        self.round_number = 0
        self.status = True
        self.leaders = []


    def start_new_round(self):
        self.round_number += 1
        self.select_leader()
        self.max_count_members = settings_lobby[self.count_players]["count_members"][self.round_number - 1]
        self.count_members = 0
        self.add_member_of_robbery(self.leaders[-1])

    
    def add_member_of_robbery(self, player_id):
        self.members[player_id] = None
        self.count_members += 1

    
    def remove_member_of_robbery(self, player_id):
        self.members.pop(player_id)
        self.count_members -= 1

    
    def member_vote(self, member_id: int, choice: bool):
        self.members[member_id] = choice


    def get_choices_of_members(self) -> bool:
        result = list(self.members.values())
        shuffle(result)
        return result


    def check_everyone_voted(self) -> bool:
        for choice in self.get_choices_of_members():
            if choice == None:
                return False
        return True
    

    def update_score(self):
        result = all(self.get_choices_of_members())
        if result:
            self.score["robbers"] += 1
            self.score["together"][self.round_number - 1] = "⬜️"
        else:
            self.score["spies"] += 1
            self.score["together"][self.round_number - 1] = "⬛️"


    def check_game_end(self) -> bool:
        return self.score["robbers"] >= 3 or self.score["spies"] >= 3
    

    def define_winner_team(self) -> str:
        if self.score["robbers"] > self.score["spies"]:
            return "robbers"
        else:
            return "spies"


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


    def reset_score(self):
        self.score["robbers"] = 0
        self.score["spies"] = 0
        self.score["together"] = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣"]


    def select_leader(self):
        random_player_id = self.select_random_player_id()
        # while random_player_id in self.leaders:
        #     random_player_id = self.select_random_player_id()
        self.leaders.append(random_player_id)


    def select_random_player_id(self) -> int:
        return choice(list(self.players.keys()))




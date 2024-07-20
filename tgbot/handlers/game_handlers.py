from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from utils.helpers import *
from utils.users import *

# TODO: ВЫНЕСТИ ТЕКСТОВЫЕ СООБЩЕНИЯ В messages.py

def register_handlers(bot: TeleBot):

    @bot.callback_query_handler(func=lambda callback: callback.data == "start_game")
    def start_game_callback(call):
        if check_admin_lobby(call.from_user.id):
            chat_id = get_chat_id(call.from_user.id)
            lobby = start(chat_id)

            for player_id, role in lobby.players.items():
                bot.send_message(player_id, f"{role}")

            bot.send_message(chat_id, "Игра началась")
            start_new_round_function(lobby)
        else:
            bot.delete_message(call.from_user.id, call.message.id)


    def start_new_round_function(lobby: Lobby):
        bot.send_message(lobby.chat_id, lobby.game.score['together'])
        leader = get_info_user(lobby.game.leaders[-1])

        bot.send_message(lobby.chat_id, f"Лидер - {leader["NAME"]}")
        bot.send_message(lobby.game.leaders[-1], "Вы лидер")


    @bot.callback_query_handler
    
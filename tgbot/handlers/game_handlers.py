from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from tgbot.handlers.messages import MessageClass
from tgbot.handlers.helpers import *
from tgbot.keyboards.game_keyboards import *
from tgbot.keyboards.lobby_keyboards import *
from tgbot.filters import *
from utils.game.helpers_lobby import *
from utils.game.helpers_game import *
from utils.users.helpers import *

# TODO: ВЫНЕСТИ ТЕКСТОВЫЕ СООБЩЕНИЯ В messages.py

def register_handlers(bot: TeleBot):

    @bot.callback_query_handler(func=lambda callback: start_game_callback_filter(callback))
    def start_game_callback(call: CallbackQuery):
        creator_id, chat_id, message_id = get_attributs_from_callback(call)
        if get_count_players_lobby(chat_id) >= 1:
            bot.delete_message(creator_id, message_id)
            bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_game_keyboard())
            if not is_lobby_play(chat_id):
                start_game(chat_id)
                bot.send_message(chat_id, "Игра началась")
                for player_id, role in get_players_and_roles(chat_id).items():
                    bot.send_message(player_id, "Шпион" if role == "spy" else "Грабитель")
                start_new_round_function(chat_id)
        else:
            bot.answer_callback_query(call.id, "Минимум 5")
    

    @bot.callback_query_handler(func=lambda callback: callback.data == "finish_game")
    def finish_game_callback(call: CallbackQuery):
        creator_id, chat_id, message_id = get_attributs_from_callback(call)
        bot.send_message(chat_id, "Игра закончилась досрочно")
        finish_game(chat_id)
        bot.delete_message(creator_id, message_id)
        bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_lobby_keyboard())


    def start_new_round_function(chat_id: int):
        round_number = get_round_number(chat_id)
        if round_number != 0:
            msg = "".join(["⬜️" if choice else "⬛️" for choice in get_choices_of_members(chat_id)])
            bot.send_message(chat_id, msg)
        bot.send_message(chat_id, get_together_score(chat_id))
        if not check_end_game(chat_id):
            start_new_round(chat_id)
            leader_id = get_leader_id(chat_id)
            leader_name = get_info_about_user(leader_id).name
            bot.send_message(chat_id, f"Лидер - {leader_name}")
            bot.send_message(leader_id, f"Выберете, кого возьмете на ограбление (до {get_count_members_lobby(chat_id) - 1}):",
                            reply_markup=list_members_lobby_keyboard(chat_id))
        else:
            team_winner = get_team_winner(chat_id)
            bot.send_message(chat_id, f"Победили {team_winner}")
            finish_game_function(chat_id)

        
        def finish_game_function(chat_id: int):
            finish_game(chat_id)
            creator_id = get_cretor_id(chat_id)
            bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender, reply_markup=manage_lobby_keyboard())
    
    
    @bot.callback_query_handler(func=lambda callback: take_player_on_robbery_callback_filter(callback))
    def take_player_on_robbery_callback(call: CallbackQuery):
        leader_id, chat_id, message_id = get_attributs_from_callback(call)
        if get_current_count_members_lobby(chat_id) != get_count_members_lobby(chat_id):
            member_id = int(call.data.split('_')[1])
            add_member(member_id, chat_id)
            bot.edit_message_text(f"Выберете, кого возьмете на ограбление (до {get_count_members_lobby(chat_id) - 1}):", leader_id, message_id,
                                reply_markup=list_members_lobby_keyboard(chat_id))
        else:
            bot.answer_callback_query(call.id, "Вы выбрали максимальное количество")
        

    @bot.callback_query_handler(func=lambda callback: dont_take_player_on_robbery_callback_filter(callback))
    def dont_take_player_on_robbery_callback(call: CallbackQuery):
        leader_id, chat_id, message_id = get_attributs_from_callback(call)
        member_id = int(call.data.split('_')[1])
        remove_member(member_id, chat_id)
        bot.edit_message_text(f"Выберете, кого возьмете на ограбление (до {get_count_members_lobby(chat_id) - 1}):", leader_id, message_id,
                              reply_markup=list_members_lobby_keyboard(chat_id))


    @bot.callback_query_handler(func=lambda callback: callback.data == "accept")
    def accept_callback(call: CallbackQuery):
        creator_id, chat_id, message_id = get_attributs_from_callback(call)
        bot.delete_message(creator_id, message_id)
        msg = "На ограбление идут: "
        for member_id in get_list_members_lobby(chat_id):
            member_name = get_info_about_user(member_id).name
            msg += f"{member_name}, "
            bot.send_message(member_id, "Вы выполните свою миссию на ограблении?", reply_markup=choice_keyboard())
        msg = msg[:-2]
        bot.send_message(chat_id, msg)
        
    
    @bot.callback_query_handler(func=lambda callback: callback.data in ("choice_true", "choice_false"))
    def choice_callback(call: CallbackQuery):
        member_id, chat_id, message_id = get_attributs_from_callback(call)
        choice = call.data.split('_')[1] == "true"
        vote(member_id, chat_id, choice)
        bot.delete_message(member_id, message_id)
        bot.answer_callback_query(call.id, "Вы проголосовали. Ждите, пока проголосуют остальные")
        if check_everyone_voted(chat_id):
            sum_up_of_round(chat_id)
            start_new_round_function(chat_id)

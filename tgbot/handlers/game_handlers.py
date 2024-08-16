from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from tgbot.handlers.messages import MessageClass
from tgbot.keyboards.game_keyboards import *
from tgbot.keyboards.lobby_keyboards import *
from tgbot.filters.game_filters import *
from utils.lobby_manager import *
from utils.users_data import *

# TODO: ВЫНЕСТИ ТЕКСТОВЫЕ СООБЩЕНИЯ В messages.py

def register_handlers(bot: TeleBot):

    @bot.callback_query_handler(func=lambda callback: start_game_callback_filter(callback))
    def start_game_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)

        if lobby.status_game:
            bot.answer_callback_query(call.id, "Игра уже началась")
            bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), creator_id, message_id, reply_markup=manage_game_keyboard())
        elif lobby.count_players < 1:
            bot.answer_callback_query(call.id, "Для начала игры нужно минимум 2 человека")
        else:
            bot.delete_message(creator_id, message_id)
            bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_game_keyboard())
            lobby.start_game()
            bot.send_message(lobby.id, MessageClass.startgame_callback_group())
            for player_id in lobby.get_list_players():
                bot.send_message(player_id, MessageClass.startgame_callback_hiderole_player(), parse_mode="MarkdownV2",
                                 reply_markup=show_role_keyboard())
            start_new_round_function(lobby)


    def start_new_round_function(lobby: Lobby):
        if lobby.round_number != 0:
            bot.send_message(lobby.id, MessageClass.startround_function_showScore_group(lobby), parse_mode="MarkdownV2")
        bot.send_message(lobby.id, MessageClass.startround_function_showScoreGame_group(lobby), parse_mode="MarkdownV2")
        if not lobby.check_game_end():
            lobby.start_new_round()
            leader = find_user(lobby.leaders[-1])
            bot.send_message(lobby.id, MessageClass.startgame_callback_selectleader_group(leader.id), parse_mode="MarkdownV2")
            bot.send_message(leader.id, MessageClass.startgame_callback_selectleader_leader(lobby),
                            reply_markup=select_members_keyboard(lobby.id))
        else:
            bot.send_message(lobby.id, MessageClass.startround_function_endgame_group(lobby), parse_mode="MarkdownV2")
            finish_game_function(lobby)


    def finish_game_function(lobby: Lobby):
        lobby.finish_game()
        creator_id = lobby.creator_id
        bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_lobby_keyboard())

    
    @bot.callback_query_handler(func=lambda callback: show_role_callback_filter(callback))
    def show_role_callback(call: CallbackQuery):
        player_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(player_id)
        bot.edit_message_text(MessageClass.startgame_callback_assignroles_player(player_id, lobby), player_id, message_id, parse_mode="MarkdownV2",
                              reply_markup=hide_role_keyboard())
        
    
    @bot.callback_query_handler(func=lambda callback: hide_role_callback_filter(callback))
    def hide_role_callback(call: CallbackQuery):
        player_id = call.from_user.id
        message_id = call.message.id
        bot.edit_message_text(MessageClass.startgame_callback_hiderole_player(), player_id, message_id,
                              reply_markup=show_role_keyboard())
    
    @bot.callback_query_handler(func=lambda callback: take_player_on_robbery_callback_filter(callback))
    def take_player_on_robbery_callback(call: CallbackQuery):
        leader_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(leader_id)
        member_id = int(call.data.split('_')[1])
        if member_id not in lobby.get_list_players() or member_id in lobby.get_list_members_of_robbery():
            bot.answer_callback_query(call.id, "Обновление...")
        elif lobby.count_members == lobby.max_count_members:
            bot.answer_callback_query(call.id, "Вы выбрали максимальное количество")
        else:
            lobby.add_member_of_robbery(member_id)
        bot.edit_message_text(MessageClass.startgame_callback_selectleader_leader(lobby), leader_id, message_id,
                                reply_markup=select_members_keyboard(lobby.id))
        

    @bot.callback_query_handler(func=lambda callback: dont_take_player_on_robbery_callback_filter(callback))
    def dont_take_player_on_robbery_callback(call: CallbackQuery):
        leader_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(leader_id)
        member_id = int(call.data.split('_')[1])
        if member_id not in lobby.get_list_players() or member_id not in lobby.get_list_members_of_robbery():
            bot.answer_callback_query(call.id, "Обновление...")
        else:
            lobby.remove_member_of_robbery(member_id)
            bot.edit_message_text(MessageClass.startgame_callback_selectleader_leader(lobby), leader_id, message_id,
                                  reply_markup=select_members_keyboard(lobby.id))


    @bot.callback_query_handler(func=lambda callback: accept_callback_filter(callback))
    def accept_callback(call: CallbackQuery):
        leader_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(leader_id)

        bot.delete_message(leader_id, message_id)
        lobby.status_round = True
        msg = "На ограбление идут: "
        for member_id in lobby.get_list_members_of_robbery():
            member_name = find_user(member_id).name
            msg += f"[{member_name}](tg://user?id={leader_id}), "
            bot.send_message(member_id, "Вы выполните свою миссию на ограблении?", reply_markup=choice_keyboard())
        msg = msg[:-2]
        bot.send_message(lobby.id, msg, parse_mode="MarkdownV2")
        
    
    @bot.callback_query_handler(func=lambda callback: choice_callback_filter(callback))
    def choice_callback(call: CallbackQuery):
        member_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(member_id)
        choice = call.data.split('_')[1] == "true"

        bot.delete_message(member_id, message_id)
        bot.answer_callback_query(call.id, "Вы проголосовали. Ждите, пока проголосуют остальные")
        if lobby.members[member_id] == None:
            lobby.member_vote(member_id, choice)
            if lobby.check_everyone_voted():
                lobby.status_round = False
                lobby.update_score()
                start_new_round_function(lobby)
    

    @bot.callback_query_handler(func=lambda callback: finish_game_callback_filter(callback))
    def finish_game_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)

        bot.delete_message(creator_id, message_id)
        bot.send_message(creator_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_lobby_keyboard())
        if lobby.status_game:
            bot.send_message(lobby.id, "Игра закончилась досрочно")
            lobby.finish_game()

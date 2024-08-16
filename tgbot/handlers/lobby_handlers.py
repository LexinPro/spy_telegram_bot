from telebot import TeleBot
from telebot.types import Message

from tgbot.handlers.messages import MessageClass
from tgbot.keyboards.lobby_keyboards import *
from tgbot.keyboards.game_keyboards import manage_game_keyboard
from tgbot.keyboards.back_keyboards import back_keyboard
from tgbot.filters.lobby_filters import *
from utils.lobby_manager import *
from utils.users_data import *


def register_handlers(bot: TeleBot):

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.message_handler(commands=['play'], chat_types=['group', 'supergroup'])
    def play_command(message: Message):
        user_id = message.from_user.id
        lobby_id = message.chat.id
        
        if check_lobby_exists(lobby_id):
            text = get_existing_lobby_error_message(user_id, lobby_id)
        else:
            text = get_new_lobby_error_message(user_id)

        if text:
            send_error_message(message, text)
        else:
            handle_new_lobby(user_id, lobby_id)

    def get_existing_lobby_error_message(user_id: int, lobby_id: int) -> str:
        lobby = find_lobby(lobby_id)
        if user_id == lobby.creator_id:
            return MessageClass.play_command_error_lobbyCreatedByUser_group()
        if user_id in lobby.get_list_players():
            return MessageClass.play_command_error_userInLobby_group()
        return MessageClass.play_command_error_lobbyExist_group()

    def get_new_lobby_error_message(user_id: int) -> str:
        user = find_user(user_id)
        if user.is_playing:
            return MessageClass.play_command_error_userPlayInOtherLobby_group()
        return None

    def handle_new_lobby(user_id: int, lobby_id: int):
        create_lobby(user_id, lobby_id)
        bot.send_message(lobby_id, MessageClass.play_command_createLobby_group(user_id), parse_mode='MarkdownV2')
        bot.send_message(user_id, MessageClass.play_command_createLobby_sender(), reply_markup=manage_lobby_keyboard())

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.message_handler(commands=['lobby'], chat_types=['private'])
    def lobby_command(message: Message):
        user_id = message.from_user.id
        user = find_user(user_id)
        lobby_id = user.lobby_id
        if not check_lobby_exists(lobby_id) or not is_creator_of_lobby(user_id):
            send_error_message(message, MessageClass.lobby_command_error_userNotCreator_sender())
        else:
            bot.delete_message(user_id, message.id)
            lobby = fetch_lobby(user_id)
            keyboard = manage_game_keyboard() if lobby.status_game else manage_lobby_keyboard()
            bot.send_message(user_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=keyboard)

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.message_handler(commands=['join'], chat_types=['group', 'supergroup'])
    def join_command(message: Message):
        user_id = message.from_user.id
        user = find_user(user_id)
        lobby_id = message.chat.id
        lobby = find_lobby(lobby_id)
        text = get_join_error_message(user, lobby)
        if text:
            send_error_message(message, text)
        else:
            process_user_joining(user, lobby)

    def get_join_error_message(user: UserOfTelegramBot, lobby: Lobby) -> str:
        if lobby == None:
            return MessageClass.join_command_error_lobbyNotExist_group()
        #!!!!!
        if lobby.status_game:
            return MessageClass.join_command_error_lobbyPlay_group()
        if user.is_playing:
            if user.lobby_id == lobby.id:
                return MessageClass.join_command_error_userPlayInThisLobby_group()
            return MessageClass.join_command_error_userPlayInOtherLobby_group()
        if lobby.count_players == 10:
            return MessageClass.join_command_error_lobbyFull_group()
        return None

    def process_user_joining(user: UserOfTelegramBot, lobby: Lobby):
        user.join_to_lobby(lobby.id)
        lobby.add_player(user.id)
        bot.send_message(lobby.id, MessageClass.join_command_sender(user.id), parse_mode='MarkdownV2')

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.message_handler(commands=['leave', 'quit'], chat_types=['private', 'group', 'supergroup'])
    def leave_command(message: Message):
        user_id = message.from_user.id
        chat_id = message.chat.id
        chat_type = message.chat.type

        user = find_user(user_id)
        lobby = find_lobby(user.lobby_id) if user.is_playing else None

        text = get_leave_error_message(user, lobby, chat_id, chat_type)
        if text:
            send_error_message(message, text)
        else:
            handle_user_leaving(user, lobby)

    def get_leave_error_message(user: UserOfTelegramBot, lobby: Lobby, chat_id: int, chat_type: str) -> str:
        if not user.is_playing:
            return MessageClass.leave_command_error_userNotPlay_sender()
        if chat_type in ['group', 'supergroup'] and user.lobby_id != chat_id:
            return MessageClass.leave_command_error_userInOtherLobby_sender()
        if user.id == lobby.creator_id:
            return MessageClass.leave_command_error_userIsCreatorLobby_sender()
        #!!!
        if lobby.status_game:
            return MessageClass.leave_command_error_lobbyPlay_sender()
        return None

    def handle_user_leaving(user: UserOfTelegramBot, lobby: Lobby):
        user.leave_from_lobby()
        lobby.remove_player(user.id)
        bot.send_message(lobby.id, MessageClass.leave_command_group(user.id), parse_mode='MarkdownV2')
        bot.send_message(user.id, MessageClass.leave_command_sender())

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.message_handler(commands=['kick'], chat_types=['group', 'supergroup'])
    def kick_command(message: Message):
        creator_id = message.from_user.id
        creator = find_user(creator_id)
        lobby = find_lobby(message.chat.id)

        text = get_kick_error_message(creator, lobby, message)
        if text:
            send_error_message(message, text)
        else:
            handle_user_kicking(lobby, message.reply_to_message.from_user.id)

    def get_kick_error_message(creator: UserOfTelegramBot, lobby: Lobby, message: Message) -> str:
        if lobby is None or creator.id != lobby.creator_id:
            return MessageClass.kick_command_error_userIsNotCreatorLobby_group()
        if lobby.status_game:
            return MessageClass.kick_command_error_lobbyPlay_group()
        if message.reply_to_message is None:
            return MessageClass.kick_command_error_messageNotReply_group()
        
        kicked_user_id = message.reply_to_message.from_user.id
        if kicked_user_id not in lobby.get_list_players():
            return MessageClass.kick_command_error_kickedUserNotInLobby_group()
        if kicked_user_id == creator.id:
            return MessageClass.kick_command_error_kickedUserIsCreator_group()
        return None

    def handle_user_kicking(lobby: Lobby, kicked_user_id: int):
        kicked_user = find_user(kicked_user_id)
        kicked_user.leave_from_lobby()
        lobby.remove_player(kicked_user.id)
        bot.send_message(lobby.id, MessageClass.kick_command_group(kicked_user.id), parse_mode='MarkdownV2')
            
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.callback_query_handler(func=lambda callback: list_players_callback_filter(callback))
    def list_players_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)
        bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id,
                              reply_markup=list_players_keyboard(lobby.id))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.callback_query_handler(func=lambda callback: kick_confirm_callback_filter(callback))
    def kick_confirm_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)
        kicked_user_id = int(call.data.split('_')[1])
        if kicked_user_id not in lobby.get_list_players():
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_kickedUserNotInLobby_sender())
            bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id, reply_markup=list_players_keyboard(lobby.id))
        elif kicked_user_id == lobby.creator_id:
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_kickedUserIdCreator_sender())
        elif lobby.status_game:
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_lobbyPlay_sender())
        else:
            bot.edit_message_text(MessageClass.kick_callback_confirm_sender(kicked_user_id), creator_id, message_id, parse_mode="MarkdownV2",
                                    reply_markup=kick_keyboard(kicked_user_id))
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.callback_query_handler(func=lambda callback: kick_callback_filter(callback))
    def kick_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)
        kicked_user_id = int(call.data.split('_')[1])
        kicked_user = find_user(kicked_user_id)

        error_message = get_kick_callback_error_message(lobby, kicked_user)
        if error_message != None:
            send_kick_callback_error_message(call, error_message, creator_id, message_id, lobby.id)
        else:
            handle_kick(lobby, kicked_user, creator_id, message_id)

    def get_kick_callback_error_message(lobby: Lobby, kicked_user: UserOfTelegramBot) -> str:
        if kicked_user.id not in lobby.get_list_players():
            return MessageClass.kick_callback_confirm_error_kickedUserNotInLobby_sender()
        if lobby.status_game:
            return MessageClass.kick_callback_confirm_error_lobbyPlay_sender()
        return None

    def send_kick_callback_error_message(call: CallbackQuery, error_message: str, creator_id: int, message_id: int, lobby_id: int):
        bot.answer_callback_query(call.id, error_message)
        bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id, reply_markup=list_players_keyboard(lobby_id))

    def handle_kick(lobby: Lobby, kicked_user: UserOfTelegramBot, creator_id: int, message_id: int):
        kicked_user.leave_from_lobby()
        lobby.remove_player(kicked_user.id)
        bot.edit_message_text(MessageClass.kick_command_sender(kicked_user.id), creator_id, message_id, parse_mode="MarkdownV2",
                              reply_markup=back_keyboard("list_players"))
        bot.send_message(lobby.id, MessageClass.kick_command_group(kicked_user.id), parse_mode="MarkdownV2")
    
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.callback_query_handler(func=lambda callback: delete_lobby_callback_filter(callback))
    def delete_lobby_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)

        if lobby.status_game:
            bot.answer_callback_query(call.id, MessageClass.deletelobby_callback_error_lobbyPlay_sender())
            bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), creator_id, message_id, reply_markup=manage_game_keyboard())
        else:
            delete_lobby(lobby.id)
            bot.delete_message(creator_id, message_id)
            bot.answer_callback_query(call.id, MessageClass.deletelobby_callback_sender())
            bot.send_message(lobby.id, MessageClass.deletelobby_callback_group(creator_id), parse_mode="MarkdownV2")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    @bot.callback_query_handler(func=lambda callback: back_callback_filter(callback))
    def back_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        message_id = call.message.id
        lobby = fetch_lobby(creator_id)
        
        if call.data == "back_manage_lobby":
            handle_back_to_manage_lobby(call, lobby, creator_id, message_id)
        elif call.data == "back_list_players":
            handle_back_to_list_players(call, lobby)

    def handle_back_to_manage_lobby(call: CallbackQuery, lobby: Lobby, creator_id: int, message_id: int):
        if not lobby.status_game:
            bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), creator_id, message_id,
                                reply_markup=manage_lobby_keyboard())
        else:
            bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), creator_id, message_id,
                                reply_markup=manage_game_keyboard())

    def handle_back_to_list_players(call: CallbackQuery, lobby: Lobby):
        bot.edit_message_text(MessageClass.listplayers_callback_sender(), call.from_user.id, call.message.id,
                            reply_markup=list_players_keyboard(lobby.id))

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    def send_error_message(message: Message, text: str):
        bot.reply_to(message, text, parse_mode="MarkdownV2")

from telebot import TeleBot
from telebot.types import Message

from tgbot.handlers.messages import MessageClass
from tgbot.handlers.helpers import get_attributs_from_message, get_attributs_from_callback
from tgbot.keyboards.lobby_keyboards import *
from tgbot.keyboards.game_keyboards import manage_game_keyboard
from tgbot.keyboards.back_keyboards import back_keyboard
from tgbot.filters import *
from utils.game.helpers_lobby import *
from utils.users.helpers import *

def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=['play', 'create_lobby'], chat_types=['group', 'supergroup'])
    def play_command(message: Message):
        user_id, chat_id = get_attributs_from_message(message)
        if is_lobby_exist(chat_id) and not is_creator(user_id):
            bot.reply_to(message, MessageClass.play_command_error_lobbyExist_group())
        elif is_lobby_exist(chat_id) and is_creator(user_id):
            pass
        elif not is_lobby_exist(chat_id) and is_player_in_lobby(user_id):
            bot.reply_to(message, MessageClass.play_command_error_userPlayInOtherLobby_group())
        else:
            create_lobby(user_id, chat_id)
            bot.send_message(chat_id, MessageClass.play_command_createLobby_group(user_id), parse_mode='MarkdownV2')
            bot.send_message(user_id, MessageClass.play_command_createLobby_sender(), reply_markup=manage_lobby_keyboard())


    @bot.message_handler(commands=['lobby'], chat_types=['private'])
    def lobby_command(message: Message):
        user_id = message.from_user.id
        if not is_creator(user_id):
            bot.send_message(user_id, MessageClass.lobby_command_error_userNotCreator_sender())
        else:
            chat_id = get_chat_id_of_lobby(user_id)
            bot.delete_message(user_id, message.id)
            if not is_lobby_play(chat_id):
                bot.send_message(user_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_lobby_keyboard())
            # ? Надо проверить
            else:
                bot.send_message(user_id, MessageClass.lobby_command_showManageLobby_sender(), reply_markup=manage_game_keyboard())



    @bot.message_handler(commands=['join'], chat_types=['group', 'supergroup'])
    def join_command(message: Message):
        user_id, chat_id = get_attributs_from_message(message)
        if not is_lobby_exist(chat_id):
            bot.reply_to(message, MessageClass.join_command_error_lobbyNotExist_group())
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.reply_to(message, MessageClass.join_command_error_lobbyPlay_group())
        # ? Надо проверить
        elif is_player_in_lobby(user_id) and not is_player_in_lobby(user_id, chat_id):
            bot.reply_to(message, MessageClass.join_command_error_userPlayInOtherLobby_group())
        elif is_player_in_lobby(user_id) and is_player_in_lobby(user_id, chat_id):
            bot.reply_to(message, MessageClass.join_command_error_userPlayInThisLobby_group())
        else:
            join_to_lobby(user_id, chat_id)
            bot.send_message(chat_id, MessageClass.join_command_sender(user_id), parse_mode='MarkdownV2')


    @bot.message_handler(commands=['leave', 'quit'], chat_types=['private'])
    def leave_command(message: Message):
        user_id = message.from_user.id
        if is_player_in_lobby(user_id):
            chat_id = get_chat_id_of_lobby(user_id)
        if not is_player_in_lobby(user_id):
            bot.send_message(user_id, MessageClass.leave_command_error_userNotPlay_sender())
        elif is_creator(user_id):
            bot.send_message(user_id, MessageClass.leave_command_error_userIsCreatorLobby_sender())
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.send_message(user_id, MessageClass.leave_command_error_lobbyPlay_sender())
        else:
            chat_id = get_chat_id_of_lobby(message.from_user.id)
            remove_from_lobby(user_id, chat_id)
            bot.send_message(chat_id, MessageClass.leave_command_group(message.from_user.id), parse_mode='MarkdownV2')
            bot.send_message(message.from_user.id, MessageClass.leave_command_sender())
                

    @bot.message_handler(commands=['leave', 'quit'], chat_types=['group', 'supergroup'])
    def leave_command(message: Message):
        user_id, chat_id = get_attributs_from_message(message)
        if not is_player_in_lobby(user_id, chat_id):
            bot.reply_to(message, MessageClass.leave_command_error_userNotPlay_sender())
        elif is_creator(user_id):
            bot.reply_to(message, MessageClass.leave_command_error_userIsCreatorLobby_sender())
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.reply_to(message, MessageClass.leave_command_error_lobbyPlay_sender())
        else:
            remove_from_lobby(user_id, chat_id)
            bot.send_message(chat_id, MessageClass.leave_command_group(user_id), parse_mode='MarkdownV2')


    @bot.message_handler(commands=['kick'], chat_types=['group', 'supergroup'])
    def kick_command(message: Message):
        creator_id = message.from_user.id
        chat_id = message.chat.id
        if not is_lobby_exist(chat_id):
            bot.reply_to(message, MessageClass.kick_command_error_lobbyNotExist_group())
        elif not is_creator(creator_id, chat_id):
            bot.reply_to(message, MessageClass.kick_command_error_userIsNotCreatorLobby_group())
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.reply_to(message, MessageClass.kick_command_error_lobbyPlay_group())
        elif message.reply_to_message == None:
            bot.reply_to(message, MessageClass.kick_command_error_messageNotReply_group())
        else:
            kicked_user_id = message.reply_to_message.from_user.id
            if not is_player_in_lobby(kicked_user_id, chat_id):
                bot.reply_to(message, MessageClass.kick_command_error_kickedUserNotInLobby_group())
            elif kicked_user_id == creator_id:
                bot.reply_to(message, MessageClass.kick_command_error_kickedUserIsCreator_group())
            else:
                remove_from_lobby(kicked_user_id, chat_id)
                bot.send_message(chat_id, MessageClass.kick_command_group(kicked_user_id), parse_mode='MarkdownV2')
            

    @bot.callback_query_handler(func=lambda callback: list_players_callback_filter(callback))
    def list_players_callback(call: CallbackQuery):
        user_id, chat_id, message_id = get_attributs_from_callback(call)
        bot.edit_message_text(MessageClass.listplayers_callback_sender(), user_id, message_id,
                              reply_markup=list_players_keyboard(chat_id))

    
    @bot.callback_query_handler(func=lambda callback: kick_confirm_callback_filter(callback))
    def kick_confirm_callback(call: CallbackQuery):
        creator_id, chat_id, message_id = get_attributs_from_callback(call)
        kicked_user_id = int(call.data.split('_')[1])
        if not is_player_in_lobby(kicked_user_id, chat_id):
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_kickedUserNotInLobby_sender())
            bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id,
                              reply_markup=list_players_keyboard(chat_id))
        elif is_creator(kicked_user_id, chat_id):
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_kickedUserIdCreator_sender())
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_lobbyPlay_sender())
        else:
            bot.edit_message_text(MessageClass.kick_callback_confirm_sender(kicked_user_id), creator_id, message_id, parse_mode="MarkdownV2",
                                    reply_markup=kick_keyboard(kicked_user_id))
    

    @bot.callback_query_handler(func=lambda callback: kick_callback_filter(callback))
    def kick_callback(call):
        creator_id, chat_id, message_id = get_attributs_from_callback(call)
        kicked_user_id = int(call.data.split('_')[1])
        if not is_player_in_lobby(kicked_user_id, chat_id):
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_kickedUserNotInLobby_sender())
            bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id,
                              reply_markup=list_players_keyboard(chat_id))
        # ? Надо проверить
        elif is_lobby_play(chat_id):
            bot.answer_callback_query(call.id, MessageClass.kick_callback_confirm_error_lobbyPlay_sender())
            bot.edit_message_text(MessageClass.listplayers_callback_sender(), creator_id, message_id,
                              reply_markup=list_players_keyboard(chat_id))
        else:
            remove_from_lobby(kicked_user_id, chat_id)
            bot.edit_message_text(MessageClass.kick_command_sender(kicked_user_id), creator_id, message_id, parse_mode="MarkdownV2",
                                    reply_markup=back_keyboard("list_players"))
            bot.send_message(chat_id, MessageClass.kick_command_group(kicked_user_id), parse_mode="MarkdownV2")
    

    @bot.callback_query_handler(func=lambda callback: back_callback_filter(callback))
    def back_callback(call: CallbackQuery):
        user_id, chat_id, message_id = get_attributs_from_callback(call)
        if call.data == "back_to_manage_lobby":
            if not is_lobby_play(chat_id):
                bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), user_id, message_id,
                                        reply_markup=manage_lobby_keyboard())
            else:
                bot.edit_message_text(MessageClass.lobby_command_showManageLobby_sender(), user_id, message_id,
                                        reply_markup=manage_game_keyboard())
        if call.data == "back_to_list_players":
            bot.edit_message_text(MessageClass.listplayers_callback_sender(), call.from_user.id, call.message.id,
                                    reply_markup=list_players_keyboard(get_chat_id_of_lobby(call.from_user.id)))
            
    
    @bot.callback_query_handler(func=lambda callback: delete_lobby_callback_filter(callback))
    def delete_lobby_callback(call: CallbackQuery):
        creator_id = call.from_user.id
        if is_player_in_lobby(creator_id):
            chat_id = get_chat_id_of_lobby(creator_id)
        message_id = call.message.id
        if is_lobby_play(chat_id):
            pass
        else:
            delete_lobby(chat_id)
            bot.delete_message(creator_id, message_id)
            bot.answer_callback_query(call.id, MessageClass.deletelobby_callback_sender())
            bot.send_message(chat_id, MessageClass.deletelobby_callback_group(creator_id), parse_mode="MarkdownV2")


    @bot.callback_query_handler(func=lambda callback: delete_message_lobby_callback_filter(callback))
    def delete_message_lobby_callback(call: CallbackQuery):
        bot.delete_message(call.from_user.id, call.message.id)

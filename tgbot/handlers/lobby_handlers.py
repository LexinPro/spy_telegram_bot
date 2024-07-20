from telebot import TeleBot
from telebot.types import Message

from utils.helpers import *
from tgbot.handlers.messages import *
from tgbot.keyboards.inline_keyboards import *



def register_handlers(bot: TeleBot):

    @bot.message_handler(commands=['play', 'create_lobby'], chat_types=['group', 'supergroup'])
    def play_command_handler(message: Message):
        if check_player(message.from_user.id):
            bot.reply_to(message, MessageClass.join_error_player_message())
        elif check_lobby(message.chat.id):
            bot.reply_to(message, MessageClass.create_lobby_error_exist_message())
        else:
            new_lobby(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, MessageClass.create_lobby_message(message.from_user.id), parse_mode='MarkdownV2')
            bot.send_message(message.from_user.id, MessageClass.create_lobby_for_admin_message(),
                             reply_markup=manage_lobby_keyboard())


    @bot.message_handler(commands=['join'], chat_types=['group', 'supergroup'])
    def join_command_handler(message: Message):
        if check_player(message.from_user.id):
            bot.reply_to(message, MessageClass.join_error_player_message())
        elif not check_lobby(message.chat.id):
            bot.reply_to(message, MessageClass.join_error_not_exist_message())
        else:
            join(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, MessageClass.join_message(message.from_user.id), parse_mode='MarkdownV2')


    @bot.message_handler(commands=['leave', 'quit'], chat_types=['private'])
    def leave_command_handler(message: Message):
        if not check_player(message.from_user.id):
            bot.send_message(message.from_user.id, MessageClass.leave_error_not_player_message())
        else:
            result = remove(message.chat.id)
            if isinstance(result, int):
                chat_id = result
                bot.send_message(message.from_user.id, MessageClass.leave_message())
                bot.send_message(chat_id, MessageClass.leave_all_message(message.from_user.id), parse_mode='MarkdownV2')
            elif isinstance(result, Lobby):
                chat_id = result.chat_id
                bot.send_message(message.from_user.id, MessageClass.leave_message())
                bot.send_message(chat_id, MessageClass.leave_admin_message())
                

    @bot.message_handler(commands=['leave', 'quit'], chat_types=['group', 'supergroup'])
    def leave_command_handler(message: Message):
        if not check_player(message.from_user.id):
            bot.reply_to(message, MessageClass.leave_error_not_player_message())
        elif not check_lobby(message.chat.id):
            bot.reply_to(message, MessageClass.leave_error_not_exist_message())
        elif not check_player_lobby(message.from_user.id, message.chat.id):
            bot.reply_to(message, MessageClass.leave_error_not_player_this_lobby_message())
        else:
            result = remove(message.from_user.id)
            if isinstance(result, int):
                chat_id = result
                bot.send_message(chat_id, MessageClass.leave_all_message(message.from_user.id), parse_mode='MarkdownV2')
            elif isinstance(result, Lobby):
                chat_id = result.chat_id
                bot.send_message(chat_id, MessageClass.leave_admin_message())


    @bot.message_handler(commands=['kick'], chat_types=['group', 'supergroup'])
    def kick_command_handler(message: Message):
        if not check_lobby(message.chat.id):
            bot.reply_to(message, MessageClass.kick_error_not_exist_message())
        elif not check_admin_lobby(message.from_user.id, message.chat.id):
            bot.reply_to(message, MessageClass.kick_error_not_admin_message())
        elif message.reply_to_message == None:
            bot.reply_to(message, MessageClass.kick_error_not_reply_message())
        elif not check_player_lobby(message.reply_to_message.from_user.id, message.chat.id):
            bot.reply_to(message, MessageClass.kick_error_not_player_this_lobby())
        elif message.reply_to_message.from_user.id == message.from_user.id:
            bot.reply_to(message, MessageClass.kick_error_yourself_message())
        else:
            remove(message.reply_to_message.from_user.id)
            bot.send_message(message.chat.id, MessageClass.kick_message(message.reply_to_message.from_user.id),
                             parse_mode='MarkdownV2')
            

    @bot.callback_query_handler(func=lambda callback: callback.data == "list_players_lobby")
    def list_players_callback(call):
        if check_admin_lobby(call.from_user.id):
            bot.edit_message_text(MessageClass.list_players_message(), call.from_user.id, call.message.id,
                                reply_markup=list_players_keyboard(get_chat_id(call.from_user.id)))
        else:
            bot.delete_message(call.from_user.id, call.message.id)

    
    @bot.callback_query_handler(func=lambda call: "kick" in call.data)
    def kick_callback(call):
        if check_admin_lobby(call.from_user.id):
            chat_id, user_id = [int(x) for x in call.data.split('_')[1:]]
            if check_admin_lobby(user_id, chat_id):
                bot.answer_callback_query(call.id, "Вы не можете исключить самого себя")
            else:
                bot.edit_message_text(MessageClass.kick_for_admin_message(user_id), call.from_user.id,
                                      call.message.id, parse_mode="MarkdownV2",
                                      reply_markup=kick_confirm_keyboard(chat_id, user_id))
        else:
            bot.delete_message(call.from_user.id, call.message.id)
    

    @bot.callback_query_handler(func=lambda call: "confirm" in call.data)
    def kick_confirm_callback(call):
        if check_admin_lobby(call.from_user.id):
            chat_id, user_id = [int(x) for x in call.data.split('_')[1:]]
            remove(user_id)
            bot.edit_message_text(MessageClass.kick2_message(user_id), call.from_user.id, call.message.id, parse_mode="MarkdownV2",
                                  reply_markup=back_keyboard("list_players"))
            bot.send_message(chat_id, MessageClass.kick_message(user_id), parse_mode="MarkdownV2")
        else:
            bot.delete_message(call.from_user.id, call.message.id)
    

    @bot.callback_query_handler(func=lambda callback: callback.data in ("back_to_manage_lobby", "back_to_list_players"))
    def back_callback(call):
        if check_admin_lobby(call.from_user.id):
            if call.data == "back_to_manage_lobby":
                bot.edit_message_text(MessageClass.create_lobby_for_admin_message(), call.from_user.id, call.message.id,
                                      reply_markup=manage_lobby_keyboard())
            if call.data == "back_to_list_players":
                bot.edit_message_text(MessageClass.list_players_message(), call.from_user.id, call.message.id,
                                      reply_markup=list_players_keyboard(get_chat_id(call.from_user.id)))
        else:
            bot.delete_message(call.from_user.id, call.message.id)

from telebot.types import Message, CallbackQuery

from utils.game.helpers_lobby import get_chat_id_of_lobby


def get_attributs_from_message(message: Message) -> tuple:
    user_id = message.from_user.id
    chat_id = message.chat.id
    if user_id == chat_id:
        chat_id = get_chat_id_of_lobby(user_id)
    return (user_id, chat_id)


def get_attributs_from_callback(call: CallbackQuery) -> tuple:
    user_id = call.from_user.id
    chat_id = get_chat_id_of_lobby(user_id)
    message_id = call.message.id
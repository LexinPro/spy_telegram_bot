from telebot import TeleBot
from telebot.types import CallbackQuery


def register_handler(bot: TeleBot):
    
    @bot.callback_query_handler(func=lambda callback: callback)
    def delete_message_lobby_callback(call: CallbackQuery):
        bot.delete_message(call.from_user.id, call.message.id)

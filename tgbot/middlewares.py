from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, SkipHandler

from tgbot.handlers.messages import MessageClass
from utils.users import check_user

class AuthMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot):
        self.update_types = ['message']
        self.bot = bot

    def pre_process(self, message, data):
        if not check_user(message.from_user.id) and not message.text == "/start":
            self.bot.reply_to(message, MessageClass.user_is_not_auth())
            return SkipHandler()
        
            

    def post_process(self, message, data, exception):
        pass
from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, SkipHandler

from tgbot.handlers.messages import MessageClass
from utils.users_data import is_user_authorized

class AuthMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot):
        self.update_types = ['message']
        self.bot = bot

    def pre_process(self, message, data):
        if not is_user_authorized(message.from_user.id) and not message.text == "/start" and message.text[0] == '/':
            self.bot.reply_to(message, MessageClass.checkAuth_middleware_sender(), parse_mode="MarkdownV2")
            return SkipHandler()
        
    def post_process(self, message, data, exception):
        pass
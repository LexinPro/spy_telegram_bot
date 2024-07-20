from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from utils.users import *
from tgbot.config import ConfigBot
from tgbot.handlers import user_handlers, lobby_handlers, game_handlers
from tgbot.middlewares import AuthMiddleware

state_storage = StateMemoryStorage()
bot = TeleBot(ConfigBot.TOKEN, state_storage=state_storage, use_class_middlewares=True)
bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.setup_middleware(AuthMiddleware(bot))

user_handlers.register_handlers(bot)
lobby_handlers.register_handlers(bot)
game_handlers.register_handlers(bot)
from tgbot.mybot import bot
from utils.users import init_users


if __name__ == '__main__':
    init_users()
    bot.infinity_polling()


from tgbot.mybot import bot
from utils.users.helpers import initialize_users


if __name__ == '__main__':
    initialize_users()
    bot.infinity_polling()

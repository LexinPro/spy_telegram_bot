from telebot import *
from telebot.types import Message

from utils.users import *
from utils.helpers import *
from tgbot.keyboards.inline_keyboards import *
from tgbot.handlers.messages import *
from tgbot.states import *



def register_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start'], chat_types=['private'])
    def start_command_handler(message: Message):
        if not check_user(message.from_user.id):
            new_user(message.from_user.id, message.from_user.first_name)
        bot.send_message(message.from_user.id, MessageClass.hello_message())


    @bot.message_handler(commands=['info'], chat_types=['private'])
    def info_command_handler(message: Message):
        bot.send_message(message.from_user.id, MessageClass.info_message(message.from_user.id), reply_markup=info_command_keyboard())


    @bot.callback_query_handler(func=lambda callback: callback.data == "edit_name")
    def edit_name_callback(call):
        bot.delete_message(call.from_user.id, call.message.id)
        bot.send_message(call.from_user.id, MessageClass.enter_new_name_message(), reply_markup=back_keyboard("info_command"))
        bot.set_state(call.from_user.id, States.EDIT_NAME, call.message.chat.id)
    

    @bot.message_handler(state=States.EDIT_NAME, chat_types=['private'])
    def edit_name_handler(message: Message):
        rename_user(message.from_user.id, message.text)
        bot.delete_state(message.from_user.id, message.from_user.id)
        bot.edit_message_text(MessageClass.enter_new_name_message(), message.chat.id, message.id - 1)
        bot.send_message(message.from_user.id, MessageClass.edited_name_message(), reply_markup=back_keyboard("info_command"))
    

    @bot.callback_query_handler(func=lambda callback: callback.data == "edit_sex")
    def edit_sex_callback(call):
        bot.edit_message_text(MessageClass.choice_sex_message(), call.from_user.id, call.message.id, reply_markup=choice_sex_keyboard())
    

    @bot.callback_query_handler(func=lambda callback: callback.data in ("edit_sex_m", "edit_sex_w"))
    def edit_sex_callback(call):
        set_sex_user(call.from_user.id, "Мужской" if call.data == "edit_sex_m" else "Женский")
        bot.edit_message_text(MessageClass.edited_sex_message(), call.from_user.id, call.message.id, reply_markup=back_keyboard("info_command"))
    

    @bot.callback_query_handler(func=lambda callback: callback.data == "back_to_info_command", state='*')
    def back_callback(call):
        if call.data == "back_to_info_command":
            bot.delete_state(call.from_user.id, call.from_user.id)
            bot.edit_message_text(MessageClass.info_message(call.from_user.id), call.from_user.id, call.message.id, reply_markup=info_command_keyboard())
    
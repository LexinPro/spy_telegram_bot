from telebot import *
from telebot.types import Message, CallbackQuery

from utils.users.helpers import *
from utils.game.helpers_lobby import *
from tgbot.handlers.messages import *
from tgbot.keyboards.user_keyboards import *
from tgbot.keyboards.back_keyboards import back_keyboard
from tgbot.states import *



def register_handlers(bot: TeleBot):
    
    @bot.message_handler(commands=['start'], chat_types=['private'])
    def start_command(message: Message):
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        if not is_user_authorized(user_id):
            new_user(user_id, user_name)
        bot.delete_message(user_id, message.id)
        bot.send_message(user_id, MessageClass.start_command_sender())


    @bot.message_handler(commands=['info'], chat_types=['private'])
    def info_command(message: Message):
        user_id = message.from_user.id
        bot.delete_message(user_id, message.id)
        bot.send_message(user_id, MessageClass.info_command_sender(user_id), parse_mode="html", reply_markup=info_command_keyboard())


    @bot.callback_query_handler(func=lambda callback: callback.data == "edit_name")
    def enter_name_callback(call: CallbackQuery):
        user_id = call.from_user.id
        message_id = call.message.id
        bot.delete_message(user_id, message_id)
        bot.send_message(user_id, MessageClass.enterName_callback_sender(), reply_markup=back_keyboard("info_command"))
        bot.set_state(user_id, States.EDIT_NAME, user_id)
    

    @bot.message_handler(state=States.EDIT_NAME, chat_types=['private'])
    def edited_name_handler(message: Message):
        user_id = message.from_user.id
        change_name(user_id, message.text)
        bot.delete_state(user_id, user_id)
        bot.edit_message_text(MessageClass.enterName_callback_sender(), user_id, message.id - 1)
        bot.send_message(user_id, MessageClass.editedName_handler_sender(), reply_markup=back_keyboard("info_command"))
    

    @bot.callback_query_handler(func=lambda callback: callback.data == "edit_gender")
    def choice_gender_callback(call: CallbackQuery):
        user_id = call.from_user.id
        message_id = call.message.id
        bot.edit_message_text(MessageClass.choiceGender_callback_sender(), user_id, message_id, reply_markup=choice_gender_keyboard())
    

    @bot.callback_query_handler(func=lambda callback: callback.data in ("edit_gender_man", "edit_gender_woman"))
    def edited_gender_callback(call: CallbackQuery):
        user_id = call.from_user.id
        message_id = call.message.id
        change_gender(user_id, "Мужской" if call.data == "edit_gender_man" else "Женский")
        bot.edit_message_text(MessageClass.editedGender_callback_sender(), user_id, message_id, reply_markup=back_keyboard("info_command"))
    

    @bot.callback_query_handler(func=lambda callback: callback.data == "back_to_info_command", state='*')
    def back_callback(call: CallbackQuery):
        if call.data == "back_to_info_command":
            user_id = call.from_user.id
            message_id = call.message.id
            bot.delete_state(user_id, user_id)
            bot.edit_message_text(MessageClass.info_command_sender(user_id), user_id, message_id, parse_mode="html", reply_markup=info_command_keyboard())
    
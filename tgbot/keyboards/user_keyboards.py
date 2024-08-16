from telebot.util import quick_markup


def info_command_keyboard():
    keyboard = quick_markup({
        "Изменить имя": {"callback_data": "edit_name"},
        "Установить пол": {"callback_data": "edit_gender"}
    }, row_width = 1)
    return keyboard


def choice_gender_keyboard():
    keyboard = quick_markup({
        "🚹 Мужской": {"callback_data": "edit_gender_man"}, "🚺 Женский": {"callback_data": "edit_gender_woman"},
        "Назад ↩️": {"callback_data": "back_info_command"}
    }, row_width = 2)
    return keyboard

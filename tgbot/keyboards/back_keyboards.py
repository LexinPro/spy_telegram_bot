from telebot.util import quick_markup


def back_keyboard(path: str):
    keyboard = quick_markup({
        "Назад ↩️": {"callback_data": f"back_to_{path}"}
    }, row_width = 1)
    return keyboard
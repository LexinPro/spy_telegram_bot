from utils.users import *


def choice_end_by_sex(user_sex, m, w, mw):
    return m if user_sex == "Мужской" else w if user_sex == "Женский" else mw


class MessageClass:
    def hello_message() -> str:
        return "Привет, это телеграм бот ШПИОН. Добавь бота в группу и напиши команду /play\nЧтобы изменить информацию о себе - /info"
    
    def info_message(user_id: int) -> str:
        user = get_info_user(user_id)
        return f"Имя: {user["NAME"]}\nПол: {user["SEX"]}"

    def user_is_not_auth() -> str:
        return "Вы не зарегистрированы! Чтобы зарегистрироваться, введите /start в лс бота."
    
    def enter_new_name_message() -> str:
        return "Введите новое имя"
    
    def edited_name_message() -> str:
        return "Имя изменено"
    
    def choice_sex_message() -> str:
        return "Выберите пол"
    
    def edited_sex_message() -> str:
        return "Пол изменен"
    
    def create_lobby_message(user_id: int) -> str:
        user = get_info_user(user_id)
        return f"[{user["NAME"]}](tg://user?id={user_id}) создал{choice_end_by_sex(user['SEX'], '', 'а', '\(a\)')} игру\. Введите /join, чтобы присоединиться"
    
    def create_lobby_for_admin_message() -> str:
        return 'ᅠ'
    
    def create_lobby_error_exist_message() -> str:
        return "В этой группе уже создано лобби. Дождитесь, пока игра закончится"
    
    def join_message(user_id: int) -> str:
        user = get_info_user(user_id)
        return f"[{user["NAME"]}](tg://user?id={user_id}) присоединил{choice_end_by_sex(user['SEX'], 'ся', 'ась', 'ся\(ась\)')} к игре\. Чтобы выйти, введите /leave"
    
    def join_error_player_message() -> str:
        return "Вы уже играете. Напишите в личных сообщениях /leave, чтобы покинуть"
    
    def join_error_not_exist_message() -> str:
        return "В этой группе не создано лобби. Введите /play, чтобы создать"
    
    def leave_message() -> str:
        return "Вы покинули лобби"
    
    def leave_all_message(user_id: int) -> str:
        user = get_info_user(user_id)
        return f"[{user["NAME"]}](tg://user?id={user_id}) покинул{choice_end_by_sex(user['SEX'], '', 'а', '\(а\)')} лобби"
    
    def leave_admin_message() -> str:
        return "Админ лобби вышел из него, тем самым удалил лобби"
    
    def leave_error_not_player_message() -> str:
        return "Вы не находитесь в игре"
    
    def leave_error_not_player_this_lobby_message() -> str:
        return "Вы находитесь не в этой игре"
    
    def leave_error_not_exist_message() -> str:
        return "В этом чате нет активного лобби"
    
    def kick_message(kicked_user_id: int) -> str:
        kicked_user = get_info_user(kicked_user_id)
        return (f"[{kicked_user["NAME"]}](tg://user?id={kicked_user_id}) был{choice_end_by_sex(kicked_user["SEX"], '', 'а', '\(а\)')} исключен{choice_end_by_sex(kicked_user['SEX'], '', 'а', '\(а\)')} из игры")
    
    def kick2_message(kicked_user_id: int) -> str:
        kicked_user = get_info_user(kicked_user_id)
        return (f"[{kicked_user["NAME"]}](tg://openmessage?user_id={kicked_user_id}) был{choice_end_by_sex(kicked_user["SEX"], '', 'а', '\(а\)')} исключен{choice_end_by_sex(kicked_user['SEX'], '', 'а', '\(а\)')} из игры")

    def kick_for_admin_message(user_id: int) -> str:
        user = get_info_user(user_id)
        return f"Вы уверены, что хотите исключить из игры игрока [{user["NAME"]}](tg://openmessage?user_id={user_id})?"

    def kick_error_not_exist_message():
        return f"В этом чате нет активного лобби"

    def kick_error_not_admin_message():
        return f"Вы не являетесь админом этого лобби"

    def kick_error_not_reply_message():
        return f"Чтобы исключить игрока, перешлите его сообщение и напишите /kick"

    def kick_error_not_player_this_lobby():
        return f"Этот игрок не находится в лобби"

    def kick_error_yourself_message():
        return f"Нельзя исключить самого себя. Чтобы покинуть лобби, напишите /leave"
    
    def list_players_message() -> str:
        return "Чтобы кикнуть пользователя, нажмите на соответствующую игроку кнопку\nСписок игроков:"
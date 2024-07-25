from utils.users.helpers import *


def choice_ending(user_sex, m, w, mw):
    return m if user_sex == "Мужской" else w if user_sex == "Женский" else mw


"""
1. Название
2. Тип (handler/command/callback/...)
3. Контекст
4. Кому
5. Если обработка ошибки, то _error
"""


class MessageClass:

    def start_command_sender() -> str:
        return """
Добро пожаловать в игру! 🎉

Вы попали в мир захватывающих ограблений. Ваша цель – помочь команде успешно провести ограбления, но будьте осторожны, среди вас могут быть шпионы, готовые всё испортить!

Правила игры:
1. Каждый раунд один из вас становится лидером и выбирает участников для ограбления
2. Участники решают, поддержать ли ограбление или саботировать его
3. Если хоть один участник решит саботировать, ограбление провалится
Побеждает та команда, которая набрала больше побед в раундах 💰💥

Как использовать бота:
1. Добавьте бота в группу
2. Один из участников пишет /play, чтобы создать лобби
3. Остальные участники пишут /join, чтобы присоединиться к игре

Вы также можете использовать команду /info, чтобы получить сообщение с вашей личной информацией и изменить её.

Удачи, и пусть победит сильнейший!"""


    def info_command_sender(user_id: int) -> str:
        user = get_info_about_user(user_id)
        return f"""
Ваши данные:
Никнейм: {user.name}
Пол: {user.gender}

Для изменения нажмите соответствующую кнопку"""


    def checkAuth_middleware_sender() -> str:
        return """
Для того чтобы начать игру, необходимо зарегистрироваться.

Чтобы зарегистрироваться, введите команду /start в личные сообщения бота. После этого вы сможете присоединиться к игре!"""


    def enterName_callback_sender() -> str:
        return "Введите новое имя"
    
    def editedName_handler_sender() -> str:
        return "Имя изменено"
    
    def choiceGender_callback_sender() -> str:
        return "Выберите пол"
    
    def editedGender_callback_sender() -> str:
        return "Пол изменен"
    

    
    def play_command_createLobby_group(user_id: int) -> str:
        user = get_info_about_user(user_id)
        return f"""
[{user.name}](tg://user?id={user_id}) создал{choice_ending(user.gender, '', 'а', '\(a\)')} лобби\! 🎉

Чтобы присоединиться к игре, введите /join"""
    

    def play_command_createLobby_sender() -> str:
        return """
Вы успешно создали лобби! 🎉"""
    

    def play_command_error_lobbyExist_group() -> str:
        return "В этой группе уже создано лобби. Дождитесь, пока игра закончится"
    
    def play_command_error_userPlayInOtherLobby_group() -> str:
        return "Вы уже играете в другом лобби. Чтобы создать в этой группе, покиньте лобби"
    
    def lobby_command_showManageLobby_sender() -> str:
        return "ᅠ"
    
    def lobby_command_error_userNotCreator_sender() -> str:
        return "Вы не являетесь создателем лобби"
    
    def join_command_sender(user_id: int) -> str:
        user = get_info_about_user(user_id)
        return f"""
[{user.name}](tg://user?id={user_id}) присоединил{choice_ending(user.gender, 'ся', 'ась', 'ся\(ась\)')} к игре\! 🚀

Чтобы выйти из лобби, введите /leave"""
    

    def join_command_error_lobbyNotExist_group() -> str:
        return "В этой группе не создано лобби. Введите /play, чтобы создать"
    
    def join_command_error_lobbyPlay_group() -> str:
        return "Нельзя присоединиться к лобби, так как идёт игра"

    def join_command_error_userPlayInOtherLobby_group() -> str:
        return "Вы уже в лобби другого чата! Введите /leave в личку бота, чтобы выйти"
    
    def join_command_error_userPlayInThisLobby_group() -> str:
        return "Вы уже присоединились к лобби"
    
    def leave_command_sender() -> str:
        return "Вы покинули лобби"
    
    def leave_command_group(user_id: int) -> str:
        user = get_info_about_user(user_id)
        return f"[{user.name}](tg://user?id={user_id}) покинул{choice_ending(user.gender, '', 'а', '\(а\)')} лобби 👋"
    
    def leave_command_error_userNotPlay_sender() -> str:
        return "Вы не находитесь в лобби"
    
    def leave_command_error_userIsCreatorLobby_sender() -> str:
        return "Вы являетесь создателем лобби"
    
    def leave_command_error_lobbyPlay_sender() -> str:
        return "Нельзя покинуть лобби, пока идёт игра"
    
    def kick_command_group(kicked_user_id: int) -> str:
        kicked_user = get_info_about_user(kicked_user_id)
        return (f"[{kicked_user.name}](tg://user?id={kicked_user_id}) был{choice_ending(kicked_user.gender, '', 'а', '\(а\)')} исключен{choice_ending(kicked_user.gender, '', 'а', '\(а\)')} из лобби 🚫")
    
    def kick_command_sender(kicked_user_id: int) -> str:
        kicked_user = get_info_about_user(kicked_user_id)
        return (f"[{kicked_user.name}](tg://openmessage?user_id={kicked_user_id}) был{choice_ending(kicked_user.gender, '', 'а', '\(а\)')} исключен{choice_ending(kicked_user.gender, '', 'а', '\(а\)')} из лобби 🚫")

    def kick_command_error_lobbyNotExist_group() -> str:
        return "В этой группе нет лобби"
    
    def kick_command_error_userIsNotCreatorLobby_group() -> str:
        return "Вы не являетесь создателем этого лобби"
    
    def kick_command_error_lobbyPlay_group():
        return "Нельзя исключить игрока во время игры"
    
    def kick_command_error_messageNotReply_group() -> str:
        return "Чтобы исключить игрока, перешлите его сообщение и напишите /kick"
    
    def kick_command_error_kickedUserNotInLobby_group() -> str:
        return "Этот игрок не находится в лобби"
    
    def kick_command_error_kickedUserIsCreator_group() -> str:
        return "Нельзя исключить самого себя"

    def listplayers_callback_sender() -> str:
        return "Чтобы исключить пользователя, нажмите на соответствующую игроку кнопку\nСписок игроков:"

    def kick_callback_confirm_sender(kicked_user_id: int) -> str:
        kicked_user = get_info_about_user(kicked_user_id)
        return f"Вы уверены, что хотите исключить из игры игрока [{kicked_user.name}](tg://openmessage?user_id={kicked_user_id})?"

    def kick_callback_confirm_error_kickedUserNotInLobby_sender() -> str:
        return "Игрок уже не находится в лобби"

    def kick_callback_confirm_error_kickedUserIdCreator_sender() -> str:
        return "Вы не можете исключить самого себя"
    
    def kick_callback_confirm_error_lobbyPlay_sender() -> str:
        return "Вы не можете исключить игрока во время игры"

    


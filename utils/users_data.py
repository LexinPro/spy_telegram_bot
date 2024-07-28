from utils.models import UserOfTelegramBot, users


path = "utils/users/users.csv"


def initialize_users():
    with open(path, 'r', encoding="UTF-8") as file:
        for line in file:
            id, name, gender = line.split(';')[:3]
            users.append(UserOfTelegramBot(int(id), name, gender))


def save_all_users():
    with open(path, 'w', encoding="UTF-8") as file:
        for user in list(users):
            file.write(str(user))


def save_user(user: UserOfTelegramBot):
    with open(path, 'a', encoding="UTF-8") as file:
        file.write(str(user))


def register_new_user(user_id: int, user_name: str):
    user = UserOfTelegramBot(user_id, user_name)
    users.append(user)
    save_user(user)


def is_user_authorized(user_id: int):
    for user in users:
        if user.id == user_id:
            return True
    return False


def find_user(user_id: int) -> UserOfTelegramBot:
    for user in users:
        if user.id == user_id:
            return user


def check_user_is_playing(user_id: int) -> bool:
    user = find_user(user_id)
    return user.is_playing

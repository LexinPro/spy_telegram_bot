from utils.users.models import UserOfTelegramBot

path = "utils/users/users.csv"
all_users = dict()


def initialize_users():
    with open(path, 'r', encoding="UTF-8") as file:
        for line in file:
            id, name, gender = line.split(';')[:3]
            all_users[int(id)] = UserOfTelegramBot(int(id), name, gender)


def write_all_users_to_file():
    with open(path, 'w', encoding="UTF-8") as file:
        for user in list(all_users.values()):
            file.write(str(user))


def write_one_user_to_file(user: UserOfTelegramBot):
    with open(path, 'a', encoding="UTF-8") as file:
        file.write(str(user))


def new_user(user_id: int, user_name: str):
    all_users[user_id] = UserOfTelegramBot(user_id, user_name)
    write_one_user_to_file(all_users[user_id])


def change_name(user_id: int, new_name: str):
    all_users[user_id].name = new_name
    write_all_users_to_file()


def change_gender(user_id: int, gender: str):
    all_users[user_id].gender = gender
    write_all_users_to_file()


def is_user_authorized(user_id: int) -> bool:
    return user_id in all_users


def get_info_about_user(user_id: int) -> UserOfTelegramBot:
    return all_users[user_id]

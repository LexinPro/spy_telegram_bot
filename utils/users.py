path = "utils/users.csv"
USERS = dict()


def init_users():
    with open(path, 'r', encoding="UTF-8") as file:
        for user in file:
            if user != '':
                user = user.split(';')
                user[0] = int(user[0])
                USERS[user[0]] = {'NAME': user[1], "SEX": user[2]}


def write_users():
    with open(path, 'w', encoding="UTF-8") as file:
        for user_id, user_info in USERS.items():
            file.writelines(f"{user_id};{user_info['NAME']};{user_info['SEX']};\n")


def new_user(user_id: int, user_name: str):
    USERS[user_id] = {
        'NAME': user_name,
        'SEX': None,
    }
    write_users()


def rename_user(user_id: int, user_new_name: str):
    USERS[user_id]['NAME'] = user_new_name
    write_users()


def set_sex_user(user_id: int, sex: str):
    USERS[user_id]['SEX'] = sex
    write_users()


def check_user(user_id: int) -> bool:
    return user_id in USERS


def get_info_user(user_id: int) -> bool:
    return USERS[user_id]

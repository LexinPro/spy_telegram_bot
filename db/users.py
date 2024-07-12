

path = "db/users.csv"
USERS = dict()


def init_users():
    with open(path, 'r', encoding="UTF-8") as file:
        for user in file:
            user = user.split(';')
            user[0] = int(user[0])
            USERS[user[0]] = {'NAME': user[1], "SEX": user[2]}

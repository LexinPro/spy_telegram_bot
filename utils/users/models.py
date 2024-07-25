class UserOfTelegramBot:
    def __init__(self, id, name, gender="Не указан"):
        self.id = id
        self.name = name
        self.gender = gender
        self.online = False


    def __str__(self):
        return f"{self.id};{self.name};{self.gender};\n"
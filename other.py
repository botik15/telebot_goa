from connect import select_db, db_tables, create_db, all_table

create_db(db_tables)  #Создает БД
all_table() #вытаскивает все данные

# Класс для сохранения данных пользователя
class UserData:
    def __init__(self):
        self.username = ""
        self.money = 0
        self.occupation = ""
        self.url = ""
        self.message_ids = ""


# Класс для сохранения данных пользователя
class UserDataDB:
    def __init__(self):
        self.data_list = []
        self.counts = 0
        self.data_url = ""

UserDataDBs = UserDataDB()
user_data = UserData()


def global_list(index):
    data_url = select_db(db_tables, index)[1]
    data_list = select_db(db_tables, index)[0]
    counts = len(data_list)
    return data_list, data_url, counts

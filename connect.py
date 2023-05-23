import psycopg2

TOKEN = '5975838004:AAEU3OWpX6z0MDJc5u--LZJ4Mvd553OHMAk'
db_tables = ["crasota_and_zdorove", "transport_and_perevozki", "remont_and_otdelka"]
# подлкючнгие к базе данных
def connect():
    return psycopg2.connect(dbname='postgress', user='postgres',
                        password='postgres', host='127.0.0.1', port=5432)


conn = connect()
cursor = conn.cursor()
def create_db(db_tables):
    for table in db_tables:
        # Создание таблицы в базе данных
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS """ + str(table) + """ (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            money INTEGER NOT NULL,
            occupation TEXT NOT NULL,
            url TEXT NOT NULL
        )
        """)
        conn.commit()




def all_table():
    cursor.execute("""select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';""")
    print(cursor.fetchall())
    conn.commit()


def select_db(db_tables, db_tables_index):
    data = []
    url = []
    cursor.execute("SELECT * FROM " + db_tables[db_tables_index])
    for item in cursor.fetchall():
        data.append(f"Имя: {item[1]}\nУслуга: {item[3]}\nЦена: {item[2]}")
        url.append(item[4])
    return data, url


# Функция для сохранения данных пользователя в базу данных
def save_user_data(chat_id, user_data, db_tables_index):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO " + str(
        db_tables[db_tables_index]) + " (username, money, occupation, url) VALUES (%s, %s, %s, %s)",
                   (user_data.username, user_data.money, user_data.occupation, user_data.url))
    conn.commit()

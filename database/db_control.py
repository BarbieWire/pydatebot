import psycopg2


class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.__host = host
        self.__database = database
        self.__user = user
        self.__password = password
        self.__connection = None

    def connect(self):
        conn = psycopg2.connect(host=self.__host,
                                database=self.__database,
                                user=self.__user,
                                password=self.__password)
        conn.autocommit = True
        self.__connection = conn
        return self.__connection


class DatabaseControl:
    def __init__(self, conn):
        self.__connection = conn

    def create_table(self):
        with self.__connection.cursor() as curs:
            curs.execute(
                "CREATE TABLE users (chat_id int NOT NULL, photo VARCHAR, city VARCHAR, gender VARCHAR, name VARCHAR, preference VARCHAR, about VARCHAR, age INTEGER, active VARCHAR, PRIMARY KEY (chat_id))")
        return None

    def create_user(self, data: tuple) -> None:
        with self.__connection.cursor() as curs:
            curs.execute(
                "INSERT INTO users (chat_id, photo, city, gender, name, preference, about, age, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", data
            )

    def get_user(self, chat_id: int):
        with self.__connection.cursor() as curs:
            curs.execute(f"SELECT * FROM users WHERE chat_id = '{chat_id}'")
            return curs.fetchone()

    def change(self, column, data: tuple, chat_id):
        with self.__connection.cursor() as curs:
            curs.execute(f"UPDATE users SET {column} = (%s) WHERE chat_id = '{chat_id}'", data)
        return None

    def like(self, liker: int, liked: int) -> None:
        with self.__connection.cursor() as curs:
            curs.execute("INSERT INTO likes (liker, liked) VALUES (%s, %s)", (liker, liked))

    def dislike(self, data: tuple):
        with self.__connection.cursor() as curs:
            curs.execute("INSERT INTO dislikes (disliker, disliked) VALUES (%s, %s)", data)

    def search(self, chat_id, city, age, preference, gender):
        with self.__connection.cursor() as curs:
            if preference == "Both":
                curs.execute(f"SELECT * FROM users WHERE active = 'true' AND chat_id NOT IN ('{chat_id}') "
                             f"AND preference IN ('{gender}', 'Both') AND city = '{city.capitalize()}' AND age BETWEEN {age-1} AND {age+1}")
            else:
                curs.execute(f"SELECT * FROM users WHERE active = 'true' AND chat_id NOT IN ('{chat_id}') AND gender = '{preference}' "
                             f"AND preference IN ('{gender}', 'Both') AND city = '{city.capitalize()}' AND age BETWEEN {age - 1} AND {age + 1}")
            return list(curs.fetchall())

    def delete_user(self, chat_id) -> None:
        with self.__connection.cursor() as curs:
            curs.execute(f"DELETE FROM users WHERE chat_id = '{chat_id}'")

    def liked(self, chat_id) -> list:
        data = []
        with self.__connection.cursor() as curs:
            curs.execute(f"SELECT * FROM likes WHERE liked = '{chat_id}'AND mutual IS NULL ")
            for row in curs.fetchall():
                data.append(row[1])
        return data

    def liker(self, chat_id) -> list:
        data = []
        with self.__connection.cursor() as curs:
            curs.execute(f"SELECT * FROM likes WHERE mutual = 'true' AND liker = '{chat_id}'")
            for row in curs.fetchall():
                data.append(row[2])
        return data

    def set_mutual(self, liker, liked):
        with self.__connection.cursor() as curs:
            curs.execute(F"UPDATE likes SET mutual = 'true' WHERE liker = '{liker}' AND liked = '{liked}'")

    def get_mutual(self, chat_id) -> list:
        data = []
        with self.__connection.cursor() as curs:
            curs.execute(F"SELECT * FROM likes WHERE mutual = 'true' AND (liked = '{chat_id}' OR liker = '{chat_id}')")
            for row in curs.fetchall():
                if int(row[2]) != chat_id:
                    data.append(row[2])
                else:
                    data.append(row[1])
        return data

    def delete_sympathy(self, liker, liked) -> None:
        with self.__connection.cursor() as curs:
            curs.execute(F"DELETE FROM likes WHERE mutual = 'true' AND liker IN ('{liker}', '{liked}') AND liked IN ('{liker}', '{liked}')")

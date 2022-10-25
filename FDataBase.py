import sqlite3
import math
import time
import json


"""Класс FDataBase вынесен в отдельный файл чтобы разделить прямые запросы к БД и не прописывать
 их во вьюшках(обработчиках веб страниц)"""
class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):  # метод читает из таблицы БД элементы меню. В моем случае только для реализации админ доступаф
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print("Ошибка чтения из БД")
        return []

    def run_request(self, field, region, obj):  # метод добавляет в таблицу БД значения из словаря, который вернул запрос
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO result VALUES(NULL, ?, ?, ?, ?)", (field, region, obj, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления значений в таблицу БД " + str(e))
            return False
        return True

    def get_result_from_db(self):  # метод достает из базы всю таблицу и возвращает ее в виде словаря??????
        try:
            result = json.loads(self.__cur.execute("select data FROM result ORDER BY id DESC LIMIT 1").fetchone()[0])
            if result:
                return result
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД " + str(e))
        return False, False

    def add_user(self, name, email, hpsw):  # hpsw - hash password
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Пользователь с таким email уже существует")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления пользователя в БД " + str(e))
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из ДБ " + str(e))

        return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def updateUserAvatar(self, avatar, user_id):
        if not avatar:
            return False

        try:  # иначе, помещаем аватар в БД
            binary = sqlite3.Binary(avatar)  # преобразовываем аватар в бинарный объект методом Binary()
            self.__cur.execute(f"UPDATE users SET avatar = ? WHERE id = ?", (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка обновления аватара в БД: " + str(e))
            return False
        return True

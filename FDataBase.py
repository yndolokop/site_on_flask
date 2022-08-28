import sqlite3
import math
import time

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):  # метод читает из таблицы БД элементы меню.
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Ошибка чтения из БД")
        return []

    def run_request(self, name, count, percent):  # метод добавляет в таблицу БД значения из словаря, который вернул запрос
        try:
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO person VALUES(NULL, ?, ?, ?, ?)", (name, count, percent, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Ошибка добавления значений в таблицу БД "+str(e))
            return False
        return True

    def get_result_from_db(self):  # метод достает из базы всю таблицу и возвращает ее в виде словаря??????
        try:
            self.__cur.execute(f"SELECT * FROM person")
            result = self.__cur.fetchall()
            if result:
                return result
        except sqlite3.Error as e:
            print("Ошибка получения статьи из БД "+str(e))
        return (False, False)

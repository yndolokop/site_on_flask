import sqlite3
from flask import Blueprint, redirect, url_for, render_template, request, flash, session, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.search_result', 'title': 'Список запросов'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.logout', 'title': 'Выйти'}]


db = None  # переменная на соединение с БД


@admin.before_request  # выполняется перед выполнением запроса
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')  # Из глобальной g контекста приложения берем свойство 'link.db', в котором храним соединение с базой


@admin.teardown_request  # выполняется после выполнения запроса
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login/', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for(
                '.index'))  # точка указывает, что функцию прдествления следует брать из текущего блупринта c именем 'admin'
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout/', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))


@admin.route('/search-result/')
def search_result():
    if not isLogged():
        return redirect(url_for('.login'))
    list = []  # для хранения запросов
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, count, percent FROM person")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения результатов поиска из БД " + str(e))
    return render_template('admin/search_result.html', title='Список запросов', memu=menu, list=list)


@admin.route('/list-users/')  # извлекаем список пользователей из базы
def listusers():
    if not isLogged():
        return redirect(url_for('login'))
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка получения юзеров из БД " + str(e))
    return render_template('admin/listusers.html', title='Список пользователей', menu=menu, list=list)



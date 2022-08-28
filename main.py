from flask import Flask, redirect, url_for, render_template, request, session, send_file, flash, abort, g
import os
import sqlite3
from parserHH import total_vacancy, skills_search, vacancy_name_url
from FDataBase import FDataBase
from word_cloud import list_of_skills, plot_cloud, wordcloud


# from exporter import save_csv


# app = Flask(__name__)  # создаем экземпляр приложения flask
# app.config.from_object(__name__)  # создаем конфигурацию нашего приложения методом from_object


"""конфигурация"""
DATABASE = 'db/hh.sqlite'  # путь к базе данных
DEBUG = True  # режим отладки, подробное описание ошибок
SECRET_KEY = 'HSH56SH45S6H4SH46SH489H4H84J8494T'  # ключ может быть любым набором символов.

app = Flask(__name__)  # создаем экземпляр приложения flaskю
app.config.from_object(__name__)  # создаем конфигурацию нашего приложения методом from_objectю

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'db/hh.sqlite')))  # переопределим# путь к базе данных.


# Свойство root_path будет ссылаться на текущий каталог нашего приложенияю
# в flask может быть несколько WSGI приложений у которых свой рабочий каталог
# и они могут использовать свои базы данных. Для этого и служит root_path


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])  # создадим базу указав путь
    conn.row_factory = sqlite3.Row  # представляет базу данных в виде словаря, и не кортежей как обычно.
    return conn


def create_db():
    """вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:  # файл, передает параметры/скрипт для таблиц в базу
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с ДБ, если оно было установлено"""
    if hasattr(g, 'link.db'):
        g.link_db.close()


@app.route("/")  # обработчик установки соединения с базой данных
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), title='Главная')


@app.route("/run/", methods=['GET'])
def run_get():
    return render_template('form.html', title='Поиск')


@app.route("/run/", methods=['POST'])
def run_request():
    button = 'Посмотреть результат'  # ссылка на /post/ в темплейт
    db = get_db()  # соединяемся с базой данных и создаем
    dbase = FDataBase(db)  # экземпляр класса FDataBase

    text = request.form['search_by']  # достаем из формы в form.html из параметра name текст запроса
    key_count = total_vacancy(text)

    requirements = skills_search(text)  # функция парсит hh.ru
    for skl in requirements:
        result = dbase.run_request(skl['name'], skl['count'], skl['percent'])  # метод run_request класса FDataBase пишет в таблицу в БД значения из словаря requirements

        if not result:
            flash('Ошибка добавления в базу', category='error')  # flask-флеш сообщения
        else:
            flash('Резутат поиска добавлен в базу', category='success')

    plot_cloud(wordcloud.generate(str(list_of_skills(text))))  # функция plotcloud генерит картинку
    wordcloud.to_file('static/images/hp_cloud_simple.png')
    return render_template('form.html', button=button, **key_count, title='Поиск')


@app.route("/post/")  # соединяет с базой, запрашивает таблицу в базе и рендерит ее на страницу
def show_parsing_result():
    db = get_db()
    dbase = FDataBase(db)
    person = dbase.get_result_from_db()

    if not person:
        abort(404)
    return render_template('form.html', person=person)


@app.route("/contacts/", methods=["GET", "POST"])
def contacts():
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    # if request.method == 'POST':
    # print(request.form)  # проверка на метод запроса. Вернет словарь с данными из формы запроса
    # print(request.form['username'])  # или конкретно username

    return render_template('contacts.html', title='Контакты')


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return f"Профиль пользователя: {username}"


@app.route("/login/", methods=["POST", "GET"])
def login():
    if 'usserLogged' in session:
        return redirect(url_for('profile', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == 'jumbojambo' and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('profile', username=session['userLogged']))
    return render_template('login.html', title='Авторизация')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == "__main__":
    app.run(debug=True)

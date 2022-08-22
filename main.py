from flask import Flask, redirect, url_for, render_template, request, session, send_file, flash, abort
import os
import sqlite3
from parserHH import total_vacancy, skills_search
from word_cloud import *
# from exporter import save_csv

# конфигурация
DATABASE = '/db/hh.db'  # путь к базе данных
DEBUG = True                # режим отладки
SECRET_KEY = 'HSH56SH45S6H4SH46SH489H4H84J8494T'

app = Flask(__name__)  # создаем экземпляр приложения flaskю
app.config.from_object(__name__)  # создаем конфигурацию нашего приложения методом from_objectю

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'hh.db')))  # переопределим# путь к базе данных.
                                            # Свойство root_path будет ссылаться на текущий каталог нашего приложенияю
                                            # в flask может быть несколько WSGI приложений у которых свой рабочий каталог
                                            # и они могут использовать свои базы данных. Для этого и служит root_path


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])  # создадим базу указав путь
    conn.row_factory = sqlite3.Row                  # представляет базу данных в виде словаря, и не кортежей как обычно.
    return conn


def create_db():
    """вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


@app.route("/")
def index():
    return render_template('index.html', title='Главная')


@app.route("/run/")
def run_get():
    return render_template('form.html', title='Поиск')


@app.route("/run/", methods=['POST'])
def run_post():
    text = request.form['search_by']
    keyword_count = total_vacancy(text)
    # print(keyword_count)
    requirements = skills_search(text)
    # print(requirements)
    plot_cloud(wordcloud)
    wordcloud.to_file('static/images/hp_cloud_simple.png')
    return render_template('form.html', searchBy=text, keyword_count=keyword_count, requirements=requirements)


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


@app.route("/layout/")
def layout():
    return render_template('layout.html')


@app.route("/child/")
def child():
    return render_template('child.html')


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
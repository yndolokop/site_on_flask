import pprint

from flask import Flask, redirect, url_for, render_template, request, session, send_file, flash, abort, g, make_response
import os
import sqlite3
import json
from FDataBase import FDataBase
from word_cloud import plot_cloud, wordcloud
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from UserLogin import UserLogin
from forms import LoginForm
from admin.admin import admin
import hhrequest as hh
import get_IDs_by_name as id

"""конфигурация"""
DATABASE = 'db/hh.sqlite'  # путь к базе данных
DEBUG = True  # режим отладки, подробное описание ошибок
SECRET_KEY = 'HSH56SH45S6H4SH46SH489H4H84J8494T'  # ключ может быть любым набором символов.
MAX_CONTENT_LENGTH = 1024 * 1024  # максимальный объем файла в байтах. т.е. 1 мегабайт

app = Flask(__name__)  # создаем экземпляр приложения flask
app.config.from_object(__name__)  # создаем конфигурацию нашего приложения методом from_object
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'db/hh.sqlite')))  # переопределим путь к базе данных.

app.register_blueprint(admin, url_prefix='/admin/')

# Свойство root_path будет ссылаться на текущий каталог нашего приложенияю
# в flask может быть несколько WSGI приложений у которых свой рабочий каталог
# и они могут использовать свои базы данных. Для этого и служит root_path

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

find_id = id.ID()
parser = hh.Parser()


@login_manager.user_loader  # создает экземпляр класса при каждом запросе от клиента/сайта
def load_user(user_id):
    print("load user")
    return UserLogin().fromDB(user_id, dbase)


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
    if not hasattr(g, 'link_db'):  # если в глобальном объекте g контекста приложения нет свойства 'link_db'
        g.link_db = connect_db()  # то мы его создаем и там сохраняем содинение с базой данных
    return g.link_db  # иначе просто возвращает уже установленое соединение


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с ДБ, если оно было установлено"""
    if hasattr(g, 'link.db'):
        g.link_db.close()


@app.route("/")  # обработчик установки соединения с базой данных
def index():
    return render_template('index.html', title='Главная')


@app.route("/run/", methods=['GET'])
def run_get():
    drop_list = find_id.get_specialization_list()

    return render_template('form.html', drop_list=drop_list)


@app.route("/run/", methods=['POST'])
def run_request():
    button = 'Посмотреть результат'  # ссылка на /post/ в темплейт
    url = 'https://api.hh.ru/vacancies'
    field = request.form['search_by_field']
    region = request.form['region']  # достаем из формы в form.html из параметра name текст запроса
    search_name = request.form['search_by']

    region_id = find_id.get_region_id(region)
    specialization_id = find_id.get_specialization_id(field)
    params = parser.get_params_no_desc(search_name, region_id, specialization_id)

    result = parser.get_json_from_api(url, params)
    key_count = parser.total_vacancy(search_name, result)

    data = parser.skills_search(url, result, search_name, region_id, specialization_id)

    res = dbase.run_request(field, region, json.dumps(data))
    # метод run_request класса FDataBase пишет в таблицу в БД значения из словаря requirements

    if not res:
        flash('Ошибка добавления в базу', category='error')  # flask-флеш сообщения
    else:
        flash('Резутат поиска добавлен в базу', category='success')

    plot_cloud(wordcloud.generate(str(parser.list_of_skills_from_description(result))))  # функция plotcloud генерит картинку
    wordcloud.to_file('static/images/hp_cloud_simple.png')
    return render_template('form.html', button=button, **key_count, title='Поиск')


@app.route("/post/")  # соединяет с базой, запрашивает таблицу в базе и рендерит ее на страницу
def show_parsing_result():
    person = dbase.get_result_from_db()
    print(person)
    if not person:
        abort(404)
    return render_template('form.html', person=person)


@app.route("/contacts/", methods=["GET", "POST"])
@login_required  # ограничение доступа к, в данном случае, результам поиска только для залогиненых пользователей
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


@app.route("/profile/")
@login_required
def profile():
    return render_template("profile.html", title="Профиль")


@app.route("/userava/")  # по этому адрессу будет возвращаться изображение в формате png
@login_required
def userava():
    img = current_user.getAvatar(app)  # метод getAvatar прописан в классе Userlogin
    if not img:
        return ""
    h = make_response(img)
    h.headers['content-Type'] = 'image/png'
    return h


@app.route("/upload/", methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(
                file.filename):  # в этом методе проверяется что расширение файла соответствует png
            try:
                img = file.read()
                res = dbase.updateUserAvatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")

                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for('profile'))


@app.route("/login/", methods=["POST", "GET"])  # обработчик авторизации пользователя
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():  # метод проверяет отправку данных POST запроса
        user = dbase.getUserByEmail(
            form.email.data)  # смотрим данные по имейлу из базы, где .email переменная из forms.py
        if user and check_password_hash(user['psw'], form.psw.data):  # если уникальный мейл и пароль совпадают
            userlogin = UserLogin().create(user)  # и они есть в базе, юзеру предоставляется вход
            remember_me = form.remember.data  # запоминаем
            login_user(userlogin, remember=remember_me)  # и авторизуем пользователя
            return redirect(request.args.get("next") or url_for(
                'profile'))  # next - это параметр текущей страницы с которой перенаправили на логин

        flash("Неверная пара логин/пароль", "error")
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/logout/")
@login_required
def logout():
    logout_user()  # flask функция
    flash("Вы вышли из аккаунта", "success")

    return redirect(url_for('login'))


@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['username']) > 2 and len(request.form['email']) > 2 \
                and len(request.form['psw']) > 4 and request.form['psw'] == request.form['psw2']:
            hash = generate_password_hash(request.form['psw'])
            res = dbase.add_user(request.form['username'], request.form['email'], hash)
            if res:
                flash("Вы успешно зарегистрированы", category="success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", category="error")
        else:
            flash("Неверно заполнены поля", 'error')
    return render_template('register.html', title='Регистрация')


@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html', title='Страница не найдена')


if __name__ == "__main__":
    app.run(debug=True)

    app.debug = True
    app.run(host="1.1.1.0")  # host="0.0.0.0" will make the page accessable
    # by going to http://[ip]:5000/ on any computer in
    # the network.

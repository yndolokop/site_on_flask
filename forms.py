from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, InputRequired, EqualTo

"""Создаем две формы и переменные для регистрации и авторизации с помощью WTF FlaskForms"""


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[InputRequired(), Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[InputRequired(), Length(min=4, max=100, message="Пароль должен быть от "
                                                                                                "4 до 100 символлов")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от "
                                                                           "4 до 100 символлов")])
    email = StringField("Email: ", validators=[InputRequired(), Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[InputRequired(), Length(min=4, max=100, message="Пароль должен быть от "
                                                                                                "4 до 100 символлов")])
    psw2 = PasswordField("Повтор пароля: ", validators=[InputRequired(), EqualTo('psw', message="Пароли не совпадают")])
    remember = BooleanField("Запомнить", default=False)
    submit = SubmitField("Войти")


# class Form(FlaskForm):
#     field = SelectField('field', choices=[])

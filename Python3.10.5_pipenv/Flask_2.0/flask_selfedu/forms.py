from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    pwd = PasswordField('Пароль: ',
                        validators=[DataRequired(message='Неверный пароль'),
                                    Length(min=4, max=100, message='Пароль должен быть от 4 до 100 символов')])
    remember_me = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    name = StringField('Имя: ',
                       validators=[Length(min=4, max=100, message='Имя должно быть от 4 до 100 символов')])
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    pwd = PasswordField('Пароль: ',
                        validators=[DataRequired(),
                                    Length(min=4, max=100, message='Пароль должен быть от 4 до 100 символов')])
    confirm_pwd = PasswordField('Повторите пароль: ',
                                validators=[DataRequired(),
                                            EqualTo('pwd', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')


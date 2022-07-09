import sqlite3
import os

from flask import Flask, render_template, request, g, flash, abort, session, \
    url_for, redirect, make_response
from FDataBase import FDataBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, \
    current_user, logout_user
from UserLogin import UserLogin
from forms import LoginForm, RegisterForm
from admin.admin import admin

# config
DATABASE = '/tmp/flsite.db'
DEBUG = True

# Произвольный ключ, желательно сложный
# Python console
# >>> import os
# >>> os.urandom(20).hex()
SECRET_KEY = '3846e6effe31245f398254190184afd971883615'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))

app.register_blueprint(admin, url_prefix='/admin')

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'error'


@login_manager.user_loader
def load_user(user_id):
    print('load_user')
    return UserLogin().from_db(user_id, dbase)


def connect_db():
    """Соединение с БД"""
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect


def create_db():
    """Вспомогательная функция для создания таблицы БД через Python Console"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()


def get_db():
    """Создание связи с БД, если она еще не установлена"""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


dbase = None


@app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.route('/')
def index():
    return render_template('index.html', menu=dbase.get_menu(),
                           posts=dbase.get_posts_announce())


@app.route('/add_post', methods=['POST', 'GET'])
@login_required
def add_post():
    if request.method == 'POST':
        if len(request.form['post-name']) > 4 and \
                len(request.form['post-article']) > 10:
            res = dbase.add_post(request.form['post-name'],
                                 request.form['post-article'],
                                 request.form['post-url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья успешно добавлена', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')

    return render_template('add_post.html', menu=dbase.get_menu(),
                           title='Добавление статьи')


@app.route('/post/<alias>')
@login_required
def show_post(alias):
    title, article = dbase.get_post(alias)
    if not title:
        abort(404)

    return render_template('post.html', menu=dbase.get_menu(),
                           title=title, article=article)


@app.teardown_appcontext
def close_db(error):
    """Закрытие связи с БД, если она была установлена"""
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return  redirect(url_for('profile'))

    form = LoginForm()
    if form.validate_on_submit():
        user = dbase.get_user_by_email(form.email.data)
        if user and check_password_hash(user['pwd'], form.pwd.data):
            user_login = UserLogin().create(user)
            remember_me = form.remember_me.data
            login_user(user_login, remember=remember_me)
            return redirect(request.args.get('next') or url_for('profile'))

        flash('Неверная пара логин/пароль', 'error')

    return render_template('login.html', menu=dbase.get_menu(),
                           title='Авторизация', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        pwd_hash = generate_password_hash(form.pwd.data)
        res = dbase.add_user(form.name.data,
                             form.email.data, pwd_hash)
        if res:
            flash('Вы успешно зарегистрированы', 'success')
            return redirect(url_for('login'))
        else:
            flash('Ошибка при добавлении в БД', 'error')

    return render_template('register.html', menu=dbase.get_menu(),
                           title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Профиль пользователя',
                           menu=dbase.get_menu())


@app.route('/user_ava')
@login_required
def user_ava():
    img = current_user.get_avatar(app)
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-type'] = 'image/png'
    return h


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verify_ext(file.filename):
            try:
                img = file.read()
                res = dbase.update_user_avatar(img, current_user.get_id())
                if not res:
                    flash('Ошибка обновления аватара', 'error')
                flash('Аватар обновлен', 'success')
            except FileNotFoundError as e:
                flash('Ошибка чтения файла', 'error')
        else:
            flash('Ошибка обновления аватара', 'error')

    return redirect(url_for('profile'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page404.html', title='Страница не найдена',
                           menu=dbase.get_menu()), 404


'''menu = [{'name': 'Установка', 'url': 'install-flask'},
        {'name': 'Первое приложение', 'url': 'first-app'},
        {'name': 'Обратная связь', 'url': 'contact'}]'''

'''
@app.route('/about')
def about():
    return render_template('about.html', title='О сайте', menu=menu)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        if len(request.form['username']) >= 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')

    return render_template('contact.html', title='Обратная связь', menu=menu)






'''

if __name__ == '__main__':
    app.run(debug=True, port=5050)

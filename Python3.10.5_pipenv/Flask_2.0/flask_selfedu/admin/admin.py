import sqlite3

from flask import Blueprint, request, redirect, url_for, flash,\
    render_template, session, g

admin = Blueprint('admin', __name__, template_folder='templates',
                  static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def admin_logged():
    return True if session.get('admin_logged') else False


def admin_logout():
    session.pop('admin_logged', None)


menu = [{'url': 'list-pubs', 'title': 'Список статей'},
        {'url': 'user-list', 'title': 'Список пользователей'},
        {'url': 'logout', 'title': 'Выйти'}]

db = None


@admin.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardoen_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not admin_logged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=['POST', 'GET'])
def login():
    if admin_logged():
        return redirect(url_for('.index'))

    if request.method == 'POST':
        if request.form['user'] == 'admin' and \
                request.form['pwd'] == '123123':
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash('Неверная пара логин/пароль', 'error')

    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=['POST', 'GET'])
def logout():
    if not admin_logged():
        return redirect(url_for('.login'))

    admin_logout()
    return redirect(url_for('.login'))


@admin.route('/list-pubs')
def list_pubs():
    if not admin_logged():
        return redirect(url_for('.login'))

    post_list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT title, article, url FROM posts')
            post_list = cur.fetchall()
        except sqlite3.Error as e:
            print('Ошибка получения статей из БД ' + str(e))

    return render_template('admin/listpubs.html', title='Список статей',
                           menu=menu, post_list=post_list)


@admin.route('/user-list')
def user_list():
    if not admin_logged():
        return redirect(url_for('.login'))

    user_list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f'SELECT name, email '
                        f'FROM users ORDER BY create_time DESC')
            user_list = cur.fetchall()
        except sqlite3.Error as e:
            print('Ошибка получения из БД ' + str(e))

    return render_template('admin/userlist.html', title='Список пользователей',
                           menu=menu, user_list=user_list)

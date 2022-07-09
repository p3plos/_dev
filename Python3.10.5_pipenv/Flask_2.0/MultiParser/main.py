from flask import Flask, flash, render_template, request
from flaskwebgui import FlaskUI
from MultyParser import get_phone_code as pc
from art import text2art

app = Flask('__name__')
ui = FlaskUI(app, width=850, height=600)

app.secret_key = 'some_secret'

logo = text2art('MultiParser')
description = pc.__doc__


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='MultiParser')


@app.route('/MultiParser', methods=['GET', 'POST'])
def multiparser():
    if request.method == 'POST':
        user_query = request.form.get('query')
        if not user_query:
            flash('Требуется запрос')
        else:
            out = pc(user_query)
            print(user_query)
            if out == 'Неверный запрос':
                flash('Неверный запрос')
            else:
                flash(f'[+] Запрос получен - {user_query}')
                flash('[+] Идет процесс...')
                flash(f'Телефонный код страны {user_query} => {out}')
                flash(f'Работа закончена.')

    return render_template('multiparser.html', title='MultiParser',
                           logo=logo, description=description)


if __name__ == '__main__':
    #app.run(debug=True)
    ui.run()

from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
fa = FontAwesome(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://l3ns:RDddy52postgres' \
                                        '@localhost/ed_cards'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    passwd = db.Column(db.String(500), nullable=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"<Users (id='{self.id}', name='{self.name}', " \
               f"create_date='{self.create_date}')>"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        # здесь должна быть проверка корректности введенных данных
        try:
            passwd_hash = generate_password_hash(request.form['passwd'])
            u = Users(email=request.form['email'], passwd=passwd_hash)
            db.session.add(u)
            db.session.flush()

            p = Profiles(name=request.form['name'], user_id=u.id)
            db.session.add(p)
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления в БД")

        return redirect(url_for('index'))

    return render_template("register.html", title="Регистрация")


if __name__ == '__main__':
    app.run(debug=True)

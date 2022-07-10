from datetime import datetime

from flask import Flask, render_template
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
fa = FontAwesome(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://l3ns:RDddy52postgres' \
                                        '@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    create_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Users (id='{self.id}', name='{self.name}', " \
               f"create_date='{self.create_date}')>"


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

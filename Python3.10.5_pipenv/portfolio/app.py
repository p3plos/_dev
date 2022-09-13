import sys
import json
from flask import Flask, render_template
from flask_flatpages import FlatPages, pygments_style_defs
from flask_frozen import Freezer

DEBUG = True
FLATPAGES_AUTO_RELOAD = DEBUG
FLATPAGES_EXTENSION = '.md'
FLATPAGES_ROOT = 'content'
POST_DIR = 'posts'
PORT_DIR = 'portfolio'

app = Flask(__name__)
flatpages = FlatPages(app)
freezer = Freezer(app)
app.config.from_object(__name__)


@app.route('/')
def index():
    articles = [p for p in flatpages if p.path.startswith(POST_DIR)]
    articles.sort(key=lambda item: item['date'], reverse=True)

    cards = [p for p in flatpages if p.path.startswith(PORT_DIR)]
    cards.sort(key=lambda item: item['title'])

    with open('settings.txt', encoding='utf8') as config:
        data = config.read()
        settings = json.loads(data)

    tags = set()
    for p in flatpages:
        t = p.meta.get('tag')
        if t:
            tags.add(t.lower())

    return render_template('index.html', posts=articles, cards=cards, tags=tags, bigheader=True, **settings)


@app.route('/posts/<name>/')
def post(name):
    path = f'{POST_DIR}/{name}'
    article = flatpages.get_or_404(path)
    return render_template('post.html', post=article)


@app.route('/portfolio/<name>/')
def card(name):
    path = f'{PORT_DIR}/{name}'
    card = flatpages.get_or_404(path)
    return render_template('card.html', card=card)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'build':
        freezer.freeze()
    else:
        app.run(host='127.0.0.1', port=8000, debug=True)

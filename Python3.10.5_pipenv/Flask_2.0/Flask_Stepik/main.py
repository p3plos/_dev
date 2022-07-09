from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    server_msg = ''
    client_id = ''
    if request.method == 'POST':
        client_id = request.form.get('id')

        for key, value in orders.items():
            if key == int(client_id):
                server_msg = repr(orders.get(key))
                return server_msg
    else:
        server_msg = 'Ошибка'
        return server_msg

    return render_template('index.html', message=server_msg)


class Order:
    def __init__(self, id, desc, items):
        self.id = id
        self.description = desc
        self.items = items

    def __repr__(self):
        return f'<Order {self.id}: {self.items} - {self.description}>'


orders = {43: Order(43, 'Оплата картой, через почту',
                    ['Кружка', 'Майка', 'Стикеры']),
          69: Order(69, 'Оплата наличными, через почту', ['Медные диски'])}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.2', port=5050)

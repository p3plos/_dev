import requests

from bs4 import BeautifulSoup


def get_phone_code(*args):
    """ МультиПарсер

    :На входе: Название страны на любом языке, регистр не важен.
    Если вы ввели, например, Россия, как Hjccbz, парсер выполнит свою работу корректно.
    :На выходе: Телефонный код указанной страны в формате "+x", где x - переменное количество цифр.
    """
    headers = {'Accept':
                   'text/html,application/xhtml+xml,application/xml;q=0.9,'
                   'image/avif,image/webp,*/*;q=0.8',
               'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) '
                   'Gecko/20100101 Firefox/102.0'}

    url = 'https://www.google.com/search?q='
    user_query = str(args)
    g_query = url + 'телефонный+код+' + user_query
    req = requests.get(g_query, headers=headers)

    with open('req.html', 'w') as file:
        file.write(req.text)

    with open('req.html') as file:
        html = file.read()

    try:
        out = BeautifulSoup(html, 'lxml').find(class_='Z0LcW').get_text()
        return out

    except AttributeError:
        return 'Неверный запрос'


get_phone_code()

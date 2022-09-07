import json
import os
import datetime

from work_alert_bot import send_msg

import requests
from bs4 import BeautifulSoup as Soup
from tqdm import tqdm

start_time = datetime.datetime.now()

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                     'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                         ' (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}


# Функция сбора данных для дальнейшего скачивания фотографий
def collect_data():
    print('[+] Старт работы...')
    send_msg(f'[partisan@python] Старт работы {datetime.datetime.now()}...')
    file = 'data_page.json'

    # Создаю файл для сбора данных, если его нет, и создаю переменную с текущей страницей для формирования ссылки
    if not os.path.isfile(file):
        with open(file, 'w') as file:
            current_page = 0

    # Если файл уже есть, читаю его, и нахожу значение страницы, далее создаю переменную с текущей странице и прибавляю 1
    else:
        with open(file) as file:
            data = json.loads(file.read())
            current_page = data['page_number']

    var = 'coupe'
    page_number = current_page + 1
    send_msg(f'[partisan@python] Номер страницы - {page_number}')

    # Формирование целевой ссылки, с запросом из переменной var, партия фотографий на одной странице - 30 шт. и номер страницы
    url = f'https://unsplash.com/napi/search/photos?query={var}&per_page=30&page={page_number}&xp=unsplash-plus-2%3AControl'

    collected_data = []

    try:
        # Отправка get-запроса по целевой ссылке с указанием заголовков и получение ответа
        response = requests.get(url=url, headers=headers)
        print(f'[+] Доступ получен - {response}')
        send_msg(f'[partisan@python] Доступ получен - {response}')
        data = response.json().get('results')
        print('[+] Сбор данных...')
        send_msg('[partisan@python] Сбор данных...')

        # В цикле прохожу по всем данным и собираю в список, объединив в словарь порядковый номер, описание и ссылку на фотографию
        for index, item in enumerate(data):
            index += 1
            img_link = item.get('urls').get('regular')
            desc = (img_link.split('/')[3].split('?')[0] if item.get(
                'alt_description') is None else item.get('alt_description'))
            collected_data.append({'index': index,
                                   'description': desc,
                                   'img_link': img_link})

        # Формирую итоговый словарь для записи в файл
        for_out_json = {'page_number': page_number,
                        'data': collected_data}

        # Записываю собранные данные в файл формата json
        out_file = f'data_page.json'
        with open(out_file, 'w') as file:
            json.dump(for_out_json, file, indent=4, ensure_ascii=False)
        print(f'[+] Данные собраны в файл - {out_file}')
        send_msg('[partisan@python] Данные собраны в файл')

        return out_file

    except Exception as ex:
        print(ex)


# Функция сохраняет фотографии по ссылкам собранным в файл
def get_images(file):
    # Создаю папку для фотографий, если ее нет
    images_path = 'images'
    if not os.path.exists(images_path):
        os.mkdir(images_path)

    # Открываю ранее сохраненный файл с собранными данными
    with open(file) as file:
        data = json.loads(file.read())

    # В цикле прохожу по всем данным и создаю две переменные
    # В первой - ссылка на фотографию
    # Во второй - название файла (взял словарь img_link, по ключу выделил ссылку, которую разделил сначала по '/' и потом по '?')
    # Далее прохожу по ссылке и сохраняю каждую картинку в папку
    # Использую модуль tqdm для визуального отображения прогресса скачивания в терминал

    send_msg('[partisan@python] Сохранение фотографий...')

    for img_link in tqdm(data['data']):
        link = img_link['img_link']
        file_name = img_link['img_link'].split('/')[3].split('?')[0]
        with open(f'images/{file_name}.jpg', 'wb') as file:
            file.write(requests.get(link).content)

    print('[+] Работа завершена')
    send_msg('[partisan@python] Работа завершена')

    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f'Время работы: {duration}')
    send_msg(f'Время работы: {duration}')
    send_msg('--------------------------------')


def main():
    get_images(collect_data())


if __name__ == '__main__':
    main()

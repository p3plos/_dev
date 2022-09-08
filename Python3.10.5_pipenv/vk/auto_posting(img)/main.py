#!/bin/bash
#
# Авто постинг картинок в группу вк. Картинка берется из папки,
# в которую автоматически их качает другой скрипт.
# Используемая картинка удаляется. Если в папке не осталось картинок,
# запускается скрипт для парсинга новой партии картинок.
# Постинг по расписанию, четыре картинки в сутки через каждые 6 часов по МСК

import os
import sys
import json

# Получаю путь до своего скрипта парсера и импортирую его
sys.path.insert(1, os.getenv('PATH_TO_PARTISAN'))
import partisan
from work_alert_bot import send_msg

import requests

# Сохраняю в переменную название папки для фотографий.
# Проверяю если папки с таким название не существует, создаю
images_path = 'images'
if not os.path.exists(images_path):
    os.mkdir(images_path)

LIST_IMG = os.listdir(images_path)


# Функция для загрузки новой партии фотографий
def download_images():
    partisan.main()


# Проверяю если список равен нулю, это значит, что в папке с фотографиями пусто и загружаю новую партию
if len(LIST_IMG) == 0:
    print('[+] Фотографии кончились. Запуск парсера...')
    send_msg('Фотографии кончились.')
    download_images()

IMG = os.listdir(images_path)[0]

TOKEN = os.getenv('VK_TOKEN')
USER_ID = os.getenv('USER_ID')
GROUP_ID = 181059371
METHOD = ['wall.post',
          'wall.edit',
          'photos.getWallUploadServer',
          'photos.saveWallPhoto']

print('[+] Начало работы...')


# Функция, которая получает ссылку для загрузки фотографий на сервер вконтакте
def get_upload_url():
    print('[+] Получаю ссылку для загрузки...')
    vk_query = f'https://api.vk.com/method/{METHOD[2]}?' \
               f'group_id={GROUP_ID}&' \
               f'access_token={TOKEN}&v=5.131'
    upload_url = requests.post(vk_query).text
    print('[+] Ссылка получена.')
    return json.loads(upload_url)['response']['upload_url']


SERVER_URL = get_upload_url()

# Сохраняю в переменную файл, который буду постить
POST_IMG = {'photo': (f'images/{IMG}', open(f'images/{IMG}', 'rb'))}

# Удаляю этот файл из папки
os.remove(f'images/{IMG}')


# Функция, которая загружает фотографию на сервер вконтакте
def upload_img_on_server(server_url):
    print('[+] Загружаю фотографию...')
    res = requests.post(server_url, files=POST_IMG)
    print('[+] Фото загружено.')
    return json.loads(res.text)


result = upload_img_on_server(SERVER_URL)


# Функция, которая сохраняет фотографию на сервер вконтакте и возвращает айди этой фотографии
def save_img_on_server_and_get_id(result):
    print('[+] Сохраняю фото, получаю id...')
    vk_query = f'https://api.vk.com/method/{METHOD[3]}?' \
               f'group_id={GROUP_ID}&' \
               f'photo={result["photo"]}&' \
               f'hash={result["hash"]}&' \
               f'server={result["server"]}&' \
               f'access_token={TOKEN}&v=5.131'

    response = requests.post(vk_query)
    print('[+] ID получено.')
    return json.loads(response.text)['response'][0]['id']


IMG_ID = save_img_on_server_and_get_id(result)


# Функция, которая постит фотографию
def post_img():
    message = '@club181059371(◣﹏◢)'

    params = f'owner_id=-{GROUP_ID}&' \
             f'message={message}&' \
             f'attachments=photo{USER_ID}_{IMG_ID}'

    query = f'https://api.vk.com/method/' \
            f'{METHOD[0]}?{params}&access_token={TOKEN}&v=5.131'

    res = requests.post(query)
    post_id = json.loads(res.text)['response']['post_id']
    print(f'[+] Доступ получен - {res}')
    print(f'[+] Пост №{post_id} опубликован!')

    send_msg(f'[auto_posting@python] Доступ получен - {res}')
    send_msg(f'[auto_posting@python] Пост №{post_id} опубликован')
    send_msg(f'------------------------------')


if __name__ == '__main__':
    post_img()

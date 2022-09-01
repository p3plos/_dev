import json
import urllib
import requests
from login import access_token, service_access_key

headers = {'Accept':
               'text/html,application/xhtml+xml,application/xml;q=0.9,'
               'image/avif,image/webp,*/*;q=0.8',
           'User-Agent':
               'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) '
               'Gecko/20100101 Firefox/102.0'}

GROUP_ID = 181059371

METHOD = ['wall.post', 'wall.edit',
          'photos.getWallUploadServer', 'photos.saveWallPhoto']

# Открывает файл "img_links.txt" на чтение и читает все строки
with open('img_links.txt', 'r') as file:
    lines = file.readlines()

# Объявляет переменную с первой строкой(ссылка на картинку)
# из файла "img_links.txt"
img_link = lines[0]

print(img_link)

# Открывает файл "img_links.txt" на запись и стирает первую строку
with open('img_links.txt', 'w') as file:
    file.writelines(lines[1:])

# Переходит по ссылке из переменной "img_link"
# и сохраняет картинку в файл
res = urllib.request.urlopen(img_link)
with open('img.jpg', 'wb') as out:
    out.write(res.read())

img = {'photo': ('img.jpg', open(r'img.jpg', 'rb'))}

# Получает ссылку для загрузки изображений
vk_query = f'https://api.vk.com/method/{METHOD[2]}?' \
           f'group_id={GROUP_ID}&' \
           f'access_token={access_token}&v=5.131'


# Загружает изображение на url
def get_upload_url(vk_query):
    upload_url = requests.post(vk_query).text
    return json.loads(upload_url)['response']['upload_url']


server_url = get_upload_url(vk_query)


def upload_img_on_server(server_url):
    res = requests.post(server_url, files=img)
    return json.loads(res.text)


result = upload_img_on_server(server_url)

# Сохраняет фото на сервере и получает id
vk_query = f'https://api.vk.com/method/{METHOD[3]}?' \
           f'group_id={GROUP_ID}&' \
           f'photo={result["photo"]}&' \
           f'hash={result["hash"]}&' \
           f'server={result["server"]}&' \
           f'access_token={access_token}&v=5.131'

response = requests.post(vk_query)
result = json.loads(response.text)['response'][0]['id']

MESSAGE = '@club181059371(◣﹏◢)'

PARAMS = f'owner_id=-{GROUP_ID}&' \
         f'message={MESSAGE}&' \
         f'attachments=photo31677012_{result}'

query = f'https://api.vk.com/method/' \
        f'{METHOD[0]}?{PARAMS}&access_token={access_token}&v=5.131'

res = requests.post(query)
print(res, res.text, sep='\n')

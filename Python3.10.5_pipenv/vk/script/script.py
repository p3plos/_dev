# -*- coding: utf-8 -*-
import requests
import random
import os
import glob
from time import sleep

vk_key = 'c979225eef7cfe5f9c0047acbab7d3bbad826be2573b494f8ff4256de9d81ecfb37dd34d0c83786d9684e'
group_id = 181059371  # ID паблика
post_text = '@club181059371 (◣﹏◢)'
pics = glob.glob('*.jpg')


if len(pics) == 0:
    print('Нет изображений для постинга')
    exit()

pic2post = random.choice(pics)

url = 'https://api.vk.com/method/photos.getWallUploadServer?group_id=%d&v=5.28&access_token=%s' % (
    group_id, vk_key)

resp = requests.get(url).json()['response']
upload_url = resp['upload_url']
files = {'file1': open(pic2post, 'rb')}
resp = requests.post(upload_url, files=files)
resp = resp.json()
server = resp['server']
photo = resp['photo']
vkhash = resp['hash']
sleep(0.4)
url = 'https://api.vk.com/method/photos.saveWallPhoto?group_id=%s&server=%s&photo=%s&hash=%s&v=5.28&access_token=%s' % (
    group_id, server, photo, vkhash, vk_key, )
resp = requests.get(url).json()['response']
resp = resp[0]
photo_id = resp['id']
owner_id = resp['owner_id']
atts = 'photo%s_%s' % (owner_id, photo_id)
sleep(0.4)
url = 'https://api.vk.com/method/wall.post?owner_id=%s&from_group=1&attachments=%s&v=5.28&access_token=%s&message=%s' % (
    -group_id, atts, vk_key, post_text)
resp = requests.get(url).json()['response']
files = 0

os.remove(pic2post)


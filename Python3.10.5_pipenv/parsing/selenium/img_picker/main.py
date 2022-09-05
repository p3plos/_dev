import random
import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

scroll_number = 50
sleep_timer = random.randrange(1, 5)

var = 'auto coupe'
URL = f'https://ru.pinterest.com/search/pins/?q={var}'


def get_img_links(url):
    driver = webdriver.Chrome(executable_path='/home/l3ns/_dev/Python3.10.5_pipenv/img_picker/'
                                              'chromedriver/chromedriver')

    try:
        print('[+] Opening a browser with the specified url')
        driver.get(url=url)
        time.sleep(sleep_timer)

        img_link_list = []
        for _ in tqdm(range(0, scroll_number), desc='[+] Scrolling...'):
            driver.execute_script("window.scrollTo(1,100000)")
            time.sleep(sleep_timer)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            for link in tqdm(soup.find_all('img'), desc='[+] Links found and added'):
                img_link = link.get('src').replace('/236x/', '/736x/')
                if img_link not in img_link_list:
                    img_link_list.append(img_link)
            time.sleep(sleep_timer)

        with open(f'img_links.txt', "w") as file:
            for item in img_link_list:
                file.write(f'{item}\n')


    except Exception as _ex:
        print(_ex)

    finally:
        driver.close()
        driver.quit()

    return "[INFO] Links collected in the file successfully!"


def main():
    print(get_img_links(URL))


if __name__ == "__main__":
    main()

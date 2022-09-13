import os
import json
import time
import requests
import pandas as pd

KEY = os.getenv('KEY')

BASE_URL = 'https://prognoz-ligastavok.ru/version-test/api/1.1/obj/pytest'
search_options = {'key': 'query_bubble',
                   'value': 'from_python'}


def give_value(constraints):
    key = constraints['key']
    value = constraints['value']
    url_wf = f'https://prognoz-ligastavok.ru/version-test/api/1.1/wf/pytestendpoint?{key}={value}'
    response = requests.post(url_wf)
    print(response.text)


def get_data():
    cursor = 1
    remaining = 1
    data_list = []
    while remaining:
        headers = {"api_token": KEY, "cursor": str(cursor)}
        response = requests.get(BASE_URL, headers=headers)
        # print(response.text)

        chunk = response.json()['response']
        remaining = chunk['remaining']
        print(*chunk['results'], sep='\n')
        data_list.append(pd.DataFrame(chunk['results']))

        cursor += chunk['count']
        time.sleep(0.1)

    print(data_list)



if __name__ == '__main__':
    get_data()
    # give_value(search_options)

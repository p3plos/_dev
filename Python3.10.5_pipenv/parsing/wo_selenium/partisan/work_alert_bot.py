import os
import requests

TOKEN = os.getenv('TOKEN')


def send_msg(text):
    token = TOKEN
    chat_id = os.getenv('CHAT_ID')
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    return results.json()


def main():
    send_msg("Goodbye!")


if __name__ == '__main__':
    main()

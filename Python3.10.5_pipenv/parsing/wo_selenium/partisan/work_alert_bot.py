import os
import requests


def send_msg(text):
    token = os.getenv('TOKEN')
    chat_id = os.getenv('CHAT_ID')
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    return results.json()


def main():
    send_msg("Hello!")


if __name__ == '__main__':
    main()

import requests
import datetime
import time
from time import sleep

from pprint import pprint
import json

from news_update_bot import get_news
from temp_update_bot import get_temp


token = "471852578:AAHbdwKjl_wjCPD2GCsu1DnKcg8FD9DfRdA"
url = 'https://api.telegram.org/bot{}/'.format(token)
greetings = ('hello', 'hi', 'greetings', 'sup', 'olah')

def getme():
    res = requests.get(url + "getme")
    d = res.json()
    username = d['result']['username']

def get_updates(offset=None):
    while True:
        try:
            URL = url + 'getUpdates'
            if offset:
                URL += '?offset={}'.format(offset)

            res = requests.get(URL)
            while (res.status_code != 200 or len(res.json()['result']) == 0):
                sleep(1)
                res = requests.get(URL)
            print(res.url)
            return res.json()

        except:
            pass;


def get_last(data):
    results = data['result']
    count = len(results)
    last = count - 1
    last_update = results[last]
    return last_update


def get_last_id_text(updates):
    last_update = get_last(updates)
    chat_id = last_update['message']['chat']['id']
    update_id = last_update['update_id']
    last_chat_name = last_update['message']['chat']['first_name']
    try:
        text = last_update['message']['text']
    except:
        text = ''
    return chat_id, text, update_id, last_chat_name


def ask_location(chat_id):
    text = 'Send Location'
    keyboard = [[{"text": "Location", "request_location": True}]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    send_message(chat_id, text, json.dumps(reply_markup))


def get_location(update_id):
    updates = get_updates(update_id + 1)
    location = get_last(updates)['message']['location']
    chat_id, text, update_id,last_chat_name = get_last_id_text(updates)
    lat = str(location['latitude'])
    lon = str(location['longitude'])
    return lat, lon, update_id


def send_message(chat_id, text, reply_markup=None):
    URL = url + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)

    if reply_markup:
        URL += '&reply_markup={}'.format(reply_markup)
    res = requests.get(URL)

    while res.status_code != 200:
        res = requests.get(URL)

    print("status!", res.status_code)


def reply_markup_maker(data):
    keyboard = []

    for i in range(0, len(data), 2):
        key = []
        key.append(data[i].title())
        try:
            key.append(data[i + 1].title())
        except:
            pass
        keyboard.append(key)

    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)


def news_bot(chat_id, update_id, last_chat_name):
    message = 'Please select below'
    commands = ['View Top News', 'Go Back']
    reply_markup = reply_markup_maker(commands)

    send_message(chat_id, message, reply_markup)
    chat_id, text, update_id, last_chat_name = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'news':
        chat_id, text, update_id,last_chat_name = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
    print(text)

    if text.lower() == 'view top news':
        message = ''
        news = get_news()
        for i, n in enumerate(news[:10], 1):
            message += str(i) + ". " + n.text + '\n\n'
        send_message(chat_id, message)

    if text.lower() == 'go back':
        text = 'start'
        menu(chat_id, text, update_id, last_chat_name)


def weather_bot(chat_id, update_id, last_chat_name):
    message = 'Please select below'
    commands = ['Check Weather', 'Go Back']
    reply_markup = reply_markup_maker(commands)

    send_message(chat_id, message, reply_markup)
    chat_id, text, update_id, last_chat_name = get_last_id_text(get_updates(update_id + 1))

    while text.lower() == 'weather':
        chat_id, text, update_id,last_chat_name = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)
    print(text)

    if text.lower() == 'check weather':

        ask_location(chat_id)
        lat, lon, update_id = get_location(update_id)
        message = get_temp(lat, lon)
        send_message(chat_id, message)

    if text.lower() == 'go back':
        text = 'start'
        menu(chat_id, text, update_id, last_chat_name)

def welcome_bot(chat_id, commands, last_chat_name):
    text = "Welcome {}".format(last_chat_name)
    send_message(chat_id, text)
    text = '{}, Please select below'.format(last_chat_name)
    reply_markup = reply_markup_maker(commands)
    send_message(chat_id, text, reply_markup)


def start_bot(chat_id, last_chat_name):
    message = 'Hello! {}'.format(last_chat_name)
    reply_markup = reply_markup_maker(['Start'])
    send_message(chat_id, message, reply_markup)

    chat_id, text, update_id, last_chat_name = get_last_id_text(get_updates())

    while (text.lower() != 'start'):

        message = 'Please select Start, below'

        reply_markup = reply_markup_maker(['Start'])
        send_message(chat_id, message, reply_markup)

        chat_id,text,update_id,last_chat_name = get_last_id_text(get_updates(update_id+1))

    return chat_id, text, update_id


def end_note(chat_id, text, update_id, last_chat_name):
    message = '{}, Do you want to continue?'.format(last_chat_name)
    reply_markup = reply_markup_maker(['Yes', 'No'])
    send_message(chat_id, message, reply_markup)

    new_text = text
    while (text == new_text):
        chat_id, new_text, update_id,last_chat_name = get_last_id_text(get_updates(update_id + 1))
        sleep(1)

    if new_text == 'Yes':
        return 'y'
    else:
        return 'n'


def menu(chat_id, text, update_id, last_chat_name):
    commands = ['news','weather']
    welcome_bot(chat_id, commands, last_chat_name)

    while (text.lower() == 'start'):
        chat_id, text, update_id,last_chat_name = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    while text.lower() not in commands:

        chat_id, text, update_id,last_chat_name = get_last_id_text(get_updates(update_id + 1))
        sleep(0.5)

    if text.lower()=='news':
        news_bot(chat_id,update_id, last_chat_name)

    elif text.lower()=='weather':
        weather_bot(chat_id, update_id, last_chat_name)


def main():

    text = ''
    chat_id, text, update_id, last_chat_name = get_last_id_text(get_updates())
    chat_id, text, update_id = start_bot(chat_id, last_chat_name)
    # print('Started')

    while text.lower() != 'n':
        sleep(1)
        text = 'start'
        menu(chat_id, text, update_id, last_chat_name)
        text = 'n'

        chat_id, text, update_id,last_chat_name = get_last_id_text(get_updates())
        text = end_note(chat_id, text, update_id, last_chat_name)


if __name__ == '__main__':
    main()

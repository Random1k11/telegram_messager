# -*- coding: utf-8 -*-
import requests
import json

from dotenv import load_dotenv
import os
load_dotenv()
from models import DataBase
from sqlalchemy.exc import IntegrityError


class TelegramAPI:


    def __init__(self):
        _token = os.getenv('TOKEN')
        self._URL = 'https://api.telegram.org/bot' + _token + '/'


    def get_updates(self):
        url = self._URL + 'getUpdates'
        r = requests.get(url)
        self.write_json(r.json())
        return r.json()


    def send_message(self, chat_id, text='Привет я БОТ'):
        url = self._URL + 'sendMessage'
        answer = {'chat_id': chat_id, 'text':text}
        r = requests.post(url, json=answer)
        return r.json()


    def write_json(self, data, filename='answer.json'):
    	with open(filename, 'w') as f:
    	   json.dump(data, f, indent=2, ensure_ascii=False)


    def like_buttons(self, chat_id):
        text = "Choose:"
        reply_inline_markup={"inline_keyboard":[[{'text': 'Like', 'callback_data': '/pic_vote 0'}, {'text': 'Кофе', 'callback_data': '/pic_vote 1'}], [{'text': 'Кофе', 'callback_data': '/pic_vote 1'}]]}
        data = {'chat_id': chat_id, 'text': text, 'reply_markup': json.dumps(reply_inline_markup)}
        url = self._URL + 'sendMessage'
        r = requests.post(url, json=data)
        return r.json()


    def send_image_with_likes(self, chat_id, num):
        url = self._URL + "sendPhoto"
        files = {'photo': open('123.jpg', 'rb')}
        reply_inline_markup={"inline_keyboard":[[{'text': u'👍', 'callback_data': 'like'}, {'text': '👎', 'callback_data': 'dislike'}]]}
        data = {'chat_id' : chat_id, 'reply_markup': json.dumps(reply_inline_markup)}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)


    def buttons(self, chat_id):
        text = "Choose:"
        reply_inline_markup={"inline_keyboard":[[{'text': 'Погода', 'callback_data': '/pic_vote 0'}, {'text': 'Кофе', 'callback_data': '/pic_vote 1'}], [{'text': 'Кофе', 'callback_data': '/pic_vote 1'}]]}
        data = {'chat_id': chat_id, 'text': '1', 'reply_markup': json.dumps(reply_inline_markup)}
        url = self._URL + 'sendMessage'
        r = requests.post(url, json=data)
        return r.json()


    def edit_likes_markup(self, chat_id, message_id, num_likes, num_dislikes):
        reply_inline_markup={"inline_keyboard":[[{'text': u'👍 ' + str(num_likes), 'callback_data': 'like'}, {'text': '👎 ' + str(num_dislikes), 'callback_data': 'dislike'}]]}
        data = {'chat_id': chat_id, 'reply_markup': json.dumps(reply_inline_markup), 'message_id': message_id}
        url = self._URL + 'editMessageReplyMarkup'
        r = requests.post(url, data=data)
        print(r.status_code, r.reason, r.content)


    def change_numbers_of_like_on_button(self, chat_id, message_id):
        numbers_of_likes = DataBase().get_numbers_of_likes_or_dislikes('like')
        numbers_of_dislikes = DataBase().get_numbers_of_likes_or_dislikes('dislike')
        print(numbers_of_likes)
        self.edit_likes_markup(chat_id, message_id, numbers_of_likes, numbers_of_dislikes)


    def callback_handler(self):
        update = self.get_updates()
        try:
            chat_id = update['result'][-1]['callback_query']['message']['chat']['id']
            message_id = update['result'][-1]['callback_query']['message']['message_id']
            user_id = update['result'][-1]['callback_query']['from']['id']
            callback_data = update['result'][-1]['callback_query']['data']

            values = [chat_id, message_id, user_id, callback_data]
            return values

            # print(user_id)
            # data = {'chat_id': chat_id, 'reply_markup': json.dumps(reply_inline_markup), 'message_id': message_id}
            # url = self._URL + 'editMessageReplyMarkup'
            # r = requests.post(url, data=data)
            # print(r.status_code, r.reason, r.content)
        except KeyError:
            values = ''

def likes_handler():
    bot = TelegramAPI()

    while True:


        values = bot.callback_handler() #if bot.callback_handler() != None else [[range(4)]]
        print(values)
        try:
            if DataBase().check_existence_row_in_db(message_id=values[1], user_id=values[2]) == None:
                print('Записываю')
                DataBase().insert_row_to_db(values)
                bot.change_numbers_of_like_on_button(values[0], values[1])
            else:
                if values[3] ==  DataBase().get_value_from_db(message_id=values[1], user_id=values[2], value='callback_data'):
                    print(values[3])
                    DataBase().delete_row_from_db(message_id=values[1], user_id=values[2])
                    bot.change_numbers_of_like_on_button(values[0], values[1])
        except TypeError:
            pass



if __name__ == '__main__':
    likes_handler()
    # bot = TelegramAPI()

    # update = bot.get_updates()
    # bot.send_image_with_likes('-1001157951267', '123')
    # bot.callback_handler()

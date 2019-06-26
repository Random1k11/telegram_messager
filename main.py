# -*- coding: utf-8 -*-
import requests
import json

from dotenv import load_dotenv
import os
load_dotenv()


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
        reply_inline_markup={"inline_keyboard":[[{'text': u'👍', 'callback_data': '/pic_vote 0'}, {'text': '👎', 'callback_data': '/pic_vote 1'}]]}
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
        reply_inline_markup={"inline_keyboard":[[{'text': u'👍 ' + str(num_likes), 'callback_data': '/pic_vote 0'}, {'text': '👎', 'callback_data': '/pic_vote 1'}]]}
        data = {'chat_id': chat_id, 'reply_markup': json.dumps(reply_inline_markup), 'message_id': message_id}
        url = self._URL + 'editMessageReplyMarkup'
        r = requests.post(url, data=data)
        print(r.status_code, r.reason, r.content)



    def callback_handler(self):
        update = bot.get_updates()
        try:
            callback_data = update['result'][-1]['callback_query']['message']['reply_markup']['inline_keyboard'][0][0]['callback_data']
            message_id = update['result'][-1]['callback_query']['message']['message_id']
            reply_inline_markup={"inline_keyboard":[[{'text': 'Погода', 'callback_data': '/pic_vote 0'}, {'text': 'Кофе', 'callback_data': '/pic_vote 1'}], [{'text': 'Кофе', 'callback_data': '/pic_vote 1'}]]}
            chat_id = update['result'][-1]['callback_query']['message']['chat']['id']
            callback_data = update['result'][-1]['callback_query']['data']
            user_id = update['result'][-1]['callback_query']['from']['id']
            if callback_data == '/pic_vote 0':
                self.edit_likes_markup(chat_id, message_id, 5, 7)

            # print(user_id)
            # data = {'chat_id': chat_id, 'reply_markup': json.dumps(reply_inline_markup), 'message_id': message_id}
            # url = self._URL + 'editMessageReplyMarkup'
            # r = requests.post(url, data=data)
            # print(r.status_code, r.reason, r.content)
        except ValueError:
            pass




if __name__ == '__main__':
    bot = TelegramAPI()

    update = bot.get_updates()
    # bot.send_image_with_likes('-1001157951267', '123')
    bot.callback_handler()

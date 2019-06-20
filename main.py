# -*- coding: utf-8 -*-
import requests
import json

from dotenv import load_dotenv
import os
load_dotenv()


class TelegramBot:


    def __init__(self):
        token = os.getenv('TOKEN')
        self.URL = 'https://api.telegram.org/bot' + token + '/'


    def get_updates(self):
        url = self.URL + 'getUpdates'
        r = requests.get(url)
        self.write_json(r.json())
        return r.json()


    def send_message(self, chat_id, text='Привет я БОТ'):
        url = self.URL + 'sendMessage'
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
        url = self.URL + 'sendMessage'
        r = requests.post(url, json=data)
        return r.json()


    def send_image_with_likes(self, chat_id, num):
        url = self.URL + "sendPhoto"
        files = {'photo': open('123.jpg', 'rb')}
        reply_inline_markup={"inline_keyboard":[[{'text': u'👍', 'callback_data': '/pic_vote 0'}, {'text': '👎', 'callback_data': '/pic_vote 1'}]]}
        data = {'chat_id' : chat_id, 'reply_markup': json.dumps(reply_inline_markup)}
        r = requests.post(url, files=files, data=data)
        print(r.status_code, r.reason, r.content)


    def buttons(self, chat_id):
        text = "Choose:"
        reply_inline_markup={"inline_keyboard":[[{'text': 'Погода', 'callback_data': '/pic_vote 0'}, {'text': 'Кофе', 'callback_data': '/pic_vote 1'}], [{'text': 'Кофе', 'callback_data': '/pic_vote 1'}]]}
        data = {'chat_id': chat_id, 'text': '1', 'reply_markup': json.dumps(reply_inline_markup)}
        url = self.URL + 'sendMessage'
        r = requests.post(url, json=data)
        return r.json()


    def callback_handler(self):
        update = bot.get_updates()
        try:
            callback_data = update['result'][-1]['callback_query']['message']['reply_markup']['inline_keyboard'][0][0]['callback_data']
            message_id = update['result'][-1]['callback_query']['message']['message_id']
            reply_inline_markup={"inline_keyboard":[[{'text': 'Погода', 'callback_data': '/pic_vote 0'}, {'text': 'Кофе', 'callback_data': '/pic_vote 1'}], [{'text': 'Кофе', 'callback_data': '/pic_vote 1'}]]}
            chat_id = update['result'][-1]['callback_query']['message']['chat']['id']
            callback_data = update['result'][-1]['callback_query']['data']
            print(callback_data)
            data = {'chat_id': chat_id, 'reply_markup': json.dumps(reply_inline_markup), 'message_id': message_id}
            url = self.URL + 'editMessageReplyMarkup'
            # r = requests.post(url, data=data)
            # print(r.status_code, r.reason, r.content)
        except ValueError:
            pass




if __name__ == '__main__':
    bot = TelegramBot()

    update = bot.get_updates()
    bot.send_image_with_likes('-1001157951267', '123')
    bot.callback_handler()

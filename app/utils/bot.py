import logging
import requests

class Bot:
    def __init__(self, bot_id, api_key):
        self.bot_id = bot_id
        self.api_key = api_key
        self.url = 'https://api.telegram.org/bot{bot_id}:{api_key}'.format(bot_id=bot_id, api_key=api_key)

    def send_message(self, chat_id, text):
        resp = None
        try:
            req = requests.get(self.url + '/sendMessage?chat_id={chat_id}&text={text}'.format(chat_id=chat_id,
                                                                                              text=text))
            resp = req.json()
        except Exception as e:
            logging.error('Failed to send message: {e}'.format(e=e))
        return resp
import json
import logging
import datetime
from os import environ
from flask import request, jsonify
from app.utils.utils import debug
from app.utils.bot import Bot

def route_handler(app):

    @app.route('/tg/<token>', methods=['POST'])
    def telegram_callback_handler(token):
        if token != '{id}:{key}'.format(id=environ.get('TELEGRAM_BOT_ID'),
                                        key=environ.get('TELEGRAM_API_KEY')):
            return jsonify({'message': 'Permission denied'}), 403

        bot = Bot(environ.get('TELEGRAM_BOT_ID'), environ.get('TELEGRAM_API_KEY'))
        data = request.get_json(force=True)
        logging.error(data)
        if 'text' in data['message']:
            message = data['message']['text']
            fields = message.split(' ')
            if fields[0] == '/баг' or fields[0] == '/bug':
                if fields[1][0] == "@":
                    bot.send_message(data['message']['chat']['id'], 'Создаю для %s карточку О_о' % (fields[1]))
        logging.error(token)
        return '', 200

    @app.route('/jira/callback', methods=['POST'])
    def jira_callback_handler():
        return '', 200

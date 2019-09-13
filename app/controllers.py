import json
import logging
import datetime
from os import environ
from flask import request, jsonify
from app.utils.utils import debug
from app.utils.bot import Bot, Actions

def route_handler(app):

    @app.route('/tg/<token>', methods=['POST'])
    def telegram_callback_handler(token):
        if token != '{id}:{key}'.format(id=environ.get('TELEGRAM_BOT_ID'),
                                        key=environ.get('TELEGRAM_API_KEY')):
            return jsonify({'message': 'Permission denied'}), 403

        data = request.get_json(force=True)
        logging.error(data)
        logging.error(token)
        if 'message' in data and 'text' in data['message']:
            message = data['message']['text']
            actions = Actions(message, data['message']['chat']['id'])
            if actions.is_command_exists():
                actions.dispatch()
        return '', 200

    @app.route('/jira/callback', methods=['POST'])
    def jira_callback_handler():
        return '', 200

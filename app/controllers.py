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
        return '', 200

    @app.route('/jira/callback', methods=['POST'])
    def jira_callback_handler():
        return '', 200

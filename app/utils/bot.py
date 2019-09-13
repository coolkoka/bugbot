import re
import logging
import requests
from os import environ
from app.utils.jira import Jira

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

    def send_sticker(self, chat_id, sticker_id='AAQCAAOvAANOm2QCh-0yx2WLp-fR9jgOAAQBAAdtAAPnFQACFgQ'):
        resp = None
        try:
            req = requests.get(self.url + '/sendSticker?chat_id={chat_id}&sticker={sticker}'.format(chat_id=chat_id,
                                                                                              sticker=sticker_id))
            resp = req.json()
        except Exception as e:
            logging.error('Failed to send message: {e}'.format(e=e))
        return resp


class Actions:
    def __init__(self, text, chat_id):
        self.text = text
        self.chat_id = chat_id
        self.command = text.split(' ')[0] if len(text.split(' ')) else None
        self.tagged_members = re.findall(r'\@\w+', self.text)
        self.bot = Bot(environ.get('TELEGRAM_BOT_ID'), environ.get('TELEGRAM_API_KEY'))

    def is_command_exists(self):
        return True if self.command else False

    def _get_title(self):
        title = self.text.replace(self.command, '')
        title = re.sub(r'\@\w+', '', title)
        return title.strip()

    def get_search_string(self):
        search = self.text.replace(self.command, '')
        return search.strip()

    def _create_bug(self):
        try:
            logging.error(self._get_title())
            if len(self.tagged_members):
                jira = Jira()
                issues = []
                for member in self.tagged_members:
                    issue = jira.create_issue(self._get_title(), member)
                    issues.append(issue)
                self.bot.send_message(self.chat_id, 'Создаю для {members} задачи: \n{issues}'.format(
                    members=', '.join(self.tagged_members),
                    issues='\n'.join(issues)))
        except Exception as e: 
            logging.error('Failed to create bug: {e}'.format(e=e))

    def _find_issue(self):
        try:
            jira = Jira()
            issues = jira.search_issues_by_description(self.get_search_string())
            if len(issues) > 0:
                self.bot.send_message(self.chat_id, "Найденные карточки: %s" % ("\n".join(issues)))
            else:
                self.bot.send_message(self.chat_id, "Не найдено карточек по такому запросу")
        except Exception as e:
            logging.error('Failed to find issues: {e}'.format(e=e))

    def _press_f(self):
        try:
            self.bot.send_sticker(self.chat_id)
        except Exception as e:
            logging.error('Failed to press F: {e}'.format(e=e))

    def dispatch(self):
        if self.command in ['/bug', '/баг']:
            self._create_bug()
        if self.command in ['/найти', '/поиск', '/find', '/search']:
            self._find_issue()
        if self.command in ['/f', '/F', '/Ф', '/ф']:
            self._press_f()


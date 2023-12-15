from logging import StreamHandler
from src.config.read_config import config

import html
import json
import logging.config
import os
import re
import requests
import telegram

for name in [
    'asyncio', "parso.python.diff", "websockets", "tornado.application",
    "telegram.bot"
]:
    logging.getLogger(name).setLevel(logging.CRITICAL)
    logging.getLogger(name).propagate = False

# removing any previous handler
rr = logging.getLogger('root')
[rr.removeHandler(hdlr) for hdlr in rr.handlers]
logging.config.dictConfig(config["Logging"])


def escape_html(text):
    allowed_tags = {
        '<strong>', '</strong>', '<code>', '</code>', '<b>', '</b>', '<u>',
        '</u>', '<i>', '</i>', '<br>', '</br>'
    }
    re_cleaner = re.compile(
        '<[^>]*>')  # it will pick all the tag which has <tag>, </tag>.
    tags_present = re.findall(re_cleaner, text)
    extra_tags = set(tags_present).difference(allowed_tags)
    for extra_tag in extra_tags:
        new_string_value = html.escape(extra_tag)
        text = text.replace(extra_tag, new_string_value)
    return text


def notify(msg):
    # log_and_notify.info('notifying')
    msg = escape_html(msg)
    if config['Notifier']['active']:
        logging.info('Notifying Developer Team Telegram')
        token = config['Notifier']['bot_token']
        chat_id = config['Notifier']['chat_id']
        bot = telegram.Bot(token=token)
        try:
            bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.HTML)
        except Exception as ex:
            logging.exception(
                f'Error occurred while sending message on dev team. {ex}')


class NotifyHandler(StreamHandler):
    def __init__(self):
        StreamHandler.__init__(self)

    def emit(self, record):
        logging.info('Emitting record')
        if not isinstance(record.args, dict):
            record.args = {}
        msg = self.format(record)
        if record.levelno >= logging.WARNING:
            if record.levelno < logging.CRITICAL:
                msg = self.format_dev_msg(record, msg)
            notify(msg)

    def format_dev_msg(self, record: logging.LogRecord, error_msg):
        logging.info('formatting record')
        msg = '<strong>Service Name</strong>: Libarary API\n'
        msg += f'<strong>File Name:- </strong> {record.pathname}\n'
        msg += f'<strong>Function Name:- </strong> {record.funcName}\n'
        msg += f'<strong>Line Number:- </strong> {record.lineno}\n'
        msg += f'<strong>Error Message:- </strong>\n <code>{error_msg}</code>\n'
        return msg


notifier = NotifyHandler()
# notifier.setLevel(logging.ERROR)
notifier.setLevel(logging.WARNING)
log_and_notify = logging.getLogger('root')
if notifier.__class__.__name__ not in [
    handle.__class__.__name__ for handle in log_and_notify.handlers
    if hasattr(handle, '__class__')
]:
    log_and_notify.addHandler(notifier)

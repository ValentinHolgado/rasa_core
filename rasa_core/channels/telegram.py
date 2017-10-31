from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from telegram.ext import Updater, MessageHandler, Filters

from rasa_core.channels.channel import InputChannel, OutputChannel, UserMessage


class TelegramOutputChannel(OutputChannel):
    """An output channel that uses a Telegram bot to communicate."""

    def __init__(self, bot, update):
        self.bot = bot
        self.update = update

    def send_text_message(self, recipient_id, message):
        self.bot.send_message(chat_id=self.update.message.chat_id,
                              text=message)


class TelegramInputChannel(InputChannel):
    """Input channel that reads the user messages from Telegram using a bot."""

    def __init__(self, telegram_token):
        self.message_handler = None
        updater = Updater(telegram_token)

        dispatcher = updater.dispatcher
        self.bot = dispatcher.bot

        dispatcher.add_handler(MessageHandler(Filters.text, self._handle_message))

        # Start the Bot
        updater.start_polling()

    def _handle_message(self, bot, update):
        """Handle messages using a Telegram bot"""
        if self.message_handler is None:
            raise Exception("Message handler has not been assigned")
        self.message_handler(UserMessage(update.message.text, TelegramOutputChannel(bot, update)))

    def start_sync_listening(self, message_handler):
        self.message_handler = message_handler

    def start_async_listening(self, message_queue):
        self.message_handler = message_queue.enqueue

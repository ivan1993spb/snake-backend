from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import logging

from lib import settings
from lib.actors import handle_telegram_update
from lib.telegram.command import Command


WELCOME_MESSAGE = 'Welcome!\nSend an image with some faces to begin'

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


def start(update, context):
    chat_id = update.message.chat.id
    handle_telegram_update.send(chat_id, Command.START)


def rules(update, context):
    chat_id = update.message.chat.id
    handle_telegram_update.send(chat_id, Command.RULES)


def list_games(update, context):
    chat_id = update.message.chat.id
    handle_telegram_update.send(chat_id, Command.LIST_GAMES)


def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def show(update, context):
    chat_id = update.message.chat.id
    _, game_id_str = update.message.text.split('_')
    game_id = int(game_id_str)
    handle_telegram_update.send(chat_id, Command.SHOW_GAME, game_id)


def delete(update, context):
    print('delete', update.message.text)
    _, game_id_str = update.message.text.split('_')
    game_id = int(game_id_str)

    print(update, game_id)

    # delete_game_from_telegram.send(update.message.chat.id, game_id)


def main():
    # Initialize the bot
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)

    # Get the update dispatcher
    dp = updater.dispatcher

    # TODO: Add commands: help, info, create_game, delete_game, random game

    # Define command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('rules', rules))
    dp.add_handler(CommandHandler('list', list_games))
    dp.add_handler(MessageHandler(Filters.regex(r'^/show_[\d]+$'), show))

    dp.add_handler(MessageHandler(Filters.regex(r'^/delete_[\d]+$'), delete))

    # Log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

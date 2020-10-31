from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,\
    PrefixHandler

import logging

from lib import settings
from lib.actors import send_games_list_to_telegram, send_game_to_telegram, \
    delete_game_from_telegram

WELCOME_MESSAGE = 'Welcome!\nSend an image with some faces to begin'

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)
logger.setLevel(settings.LOG_LEVEL)


def start(update, context):
    logger.info('Bot Started')
    update.message.reply_text(WELCOME_MESSAGE)


def help(update, context):
    update.message.reply_text('Send an image with some faces to begin')


def list_games(update, context):
    print("ok", update.message.chat.id)
    send_games_list_to_telegram.send(update.message.chat.id, 2, 3)


def error(update, context):
    logger.warning(f'Update "{update}" caused error "{context.error}"')


def show(update, context):
    print('update', update.message.text)
    _, game_id_str = update.message.text.split('_')
    game_id = int(game_id_str)

    print(update, game_id)

    send_game_to_telegram.send(update.message.chat.id, game_id)


def catify(update, context):
    user = update.message.from_user
    update.message.reply_photo(open('output/screenshots/g11s43x22-small.jpeg', 'rb'), quote=True)
    update.message.reply_text("I'm working on it...")
    logger.info(f'Photo received from {user.first_name} {user.last_name}')


def delete(update, context):
    print('delete', update.message.text)
    _, game_id_str = update.message.text.split('_')
    game_id = int(game_id_str)

    print(update, game_id)

    delete_game_from_telegram.send(update.message.chat.id, game_id)


def main():
    # Initialize the bot
    updater = Updater(token=settings.TELEGRAM_TOKEN, use_context=True)

    # Get the update dispatcher
    dp = updater.dispatcher

    # TODO: Add commands: help, info, create_game, delete_game, random game

    # Define command handlers
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('test', catify))
    dp.add_handler(CommandHandler('list', list_games))
    dp.add_handler(MessageHandler(Filters.regex(r'^/show_[\d]+$'), show))
    dp.add_handler(MessageHandler(Filters.regex(r'^/delete_[\d]+$'), delete))

    # Log all errors
    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

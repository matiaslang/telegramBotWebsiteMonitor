import logging
from typing import Text

from telegram.bot import Bot
from telegram.update import Update
import tracker
import secrets

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue, CallbackContext

from wclass import webObjects


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    helpMessage = "Ok, so welcome to my bot. This is a bot which has polled a few websites when it started, and will compare some of the elements between newer versions to find differences, updates. \n\n Here are the available commands: \n/check - This will just poll for the changes once\n/checktimer - This will start the polling automatically, and it will poll as long as this bot is on. \n/stop - This will stop the polling described on checktimer"
    update.message.reply_text(helpMessage)


def check(update, context):
    update.message.reply_text("Starting to check for updates ...")
    for i, w in enumerate(webObjects):
        update.message.reply_text(
            str(i + 1) + "/" + str(len(webObjects)) + " processing...")

        if tracker.check(w):
            update.message.reply_text("WOW! THERE HAS BEEN A CHANGE")
            update.message.reply_text(
                "THE CHANGE HAS BEEN ON THE FOLLOWING SITE:")
            update.message.reply_text(w.url)

    update.message.reply_text("Sorry, no puppies found yet :(")


def checkRepeatetly(context):
    job = context.job  # get context
    job.context.message.reply_text("Repeating check started")
    for w in webObjects:
        if tracker.check(w):
            context.bot.send_message(job.context, text="WOHOOOOO")
            job.context.message.reply_text("WOHOOOOO")
            job.context.message.reply_text("Quickly, go to this website:")
            job.context.message.reply_text(w.url)
            # job.context.message.reply_text("WOW! THERE HAS BEEN A CHANGE")
            # job.context.message.reply_text(
            #    "THE CHANGE HAS BEEN ON THE FOLLOWING SITE:")
            # job.context.message.reply_text(w.url)

    job.context.message.reply_text("Sorry, no puppies yet found :(")


def checkTimer(update: Update, context: CallbackContext):
    update.message.reply_text(
        "We have now started the polling automatically. It will happen every six hours.")
    # job = context.job
    # context.message.reply_text(
    #   "Ok, we have started the polling. It will run every now and then, and inform you if there are any changes")
    print("Ok, timer started")
    job = context.job_queue.run_repeating(
        checkRepeatetly, 21600, context=update)


def stop(update: Update, context: CallbackContext):
    update.message.reply_text("Shutting down the automatic updates...")

    # context.message.reply_text("Updating shutting down...")
    context.job_queue.stop()


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        secrets.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("check", check))
    dp.add_handler(CommandHandler("stop", stop))
    dp.add_handler(CommandHandler("CheckTimer", checkTimer))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

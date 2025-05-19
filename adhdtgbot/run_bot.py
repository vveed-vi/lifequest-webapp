#!/usr/bin/env python
import os
import sys
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("No BOT_TOKEN found in environment. Please set it.")
    sys.exit(1)

BOT_WELCOME_MESSAGE = (
    "👋 Добро пожаловать! Чтобы начать, нажми синюю кнопку *Открыть приложение* выше.\n\n"
    "Это мини-приложение поможет тебе отслеживать привычки, вести дневник и поддерживать рутину."
)

BOT_HELP_MESSAGE = (
    "ℹ️ Бот работает как мини-приложение.\n"
    "Нажми кнопку *Открыть приложение* сверху в этом чате, чтобы запустить WebApp."
)

def start_command(update: Update, context: CallbackContext) -> None:
    logger.info(f"User {update.effective_user.id} started the bot")
    update.message.reply_text(BOT_WELCOME_MESSAGE, parse_mode="Markdown")

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(BOT_HELP_MESSAGE, parse_mode="Markdown")

def main():
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    logger.info("Starting bot...")
    updater.start_polling()
    logger.info("Bot is polling for updates")
    updater.idle()

if __name__ == "__main__":
    main()

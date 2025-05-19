#!/usr/bin/env python
import os
import logging
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, 
    MessageHandler, Filters, CallbackContext
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get the token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Bot messages
BOT_WELCOME_MESSAGE = (
    "👋 Hello! I'm your ADHD support buddy. I'm here to help you establish routines, "
    "track habits, and provide support when you need it.\n\n"
    "Here's what I can do:\n"
    "• 🌞 /morning - Start your day with a morning ritual\n"
    "• 📝 /habits - Track your daily habits\n"
    "• 🌙 /evening - Reflect on your day\n"
    "• 💬 /coach - Chat with me for support and advice\n"
    "• 📊 /stats - View your progress and streaks\n"
    "• ℹ️ /help - See all available commands\n\n"
    "Let's make today a great day!"
)

BOT_HELP_MESSAGE = (
    "🔍 *ADHD Buddy Commands*\n\n"
    "• 🌞 /morning - Start your morning ritual\n"
    "• 📝 /habits - Track your habits for today\n"
    "• 🌙 /evening - Evening reflection\n"
    "• 💬 /coach - Get supportive coaching\n"
    "• 📊 /stats - View your streaks and XP\n"
    "• ℹ️ /help - Show this help message\n\n"
    "Remember, consistency is key! Try to check in with me daily."
)

# Keyboard functions
def get_main_keyboard():
    """Create the main menu inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🌞 Morning Ritual", callback_data="morning_ritual"),
            InlineKeyboardButton("🌙 Evening Reflection", callback_data="evening_reflection")
        ],
        [
            InlineKeyboardButton("📝 Track Habits", callback_data="track_habits"),
            InlineKeyboardButton("💬 Coach", callback_data="coach")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="stats"),
            InlineKeyboardButton("ℹ️ Help", callback_data="help")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# Command handlers
def start_command(update: Update, context: CallbackContext) -> None:
    """Send a welcome message when the /start command is issued."""
    logger.debug("Start command received")
    update.message.reply_text(
        BOT_WELCOME_MESSAGE,
        reply_markup=get_main_keyboard()
    )
    logger.debug(f"Welcome message sent to user {update.effective_user.id}")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the /help command is issued."""
    update.message.reply_text(
        BOT_HELP_MESSAGE, 
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(f"You said: {update.message.text}")

def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    query.answer()
    
    if query.data == "help":
        query.edit_message_text(
            text=BOT_HELP_MESSAGE,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    else:
        query.edit_message_text(
            text=f"You selected {query.data}. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start_command))
    dispatcher.add_handler(CommandHandler("help", help_command))
    
    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    
    # Handle button presses
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    # Start the Bot
    updater.start_polling()
    logger.info("Bot started polling...")

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
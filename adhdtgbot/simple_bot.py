#!/usr/bin/env python
import os
import sys
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Get the token from environment variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("No BOT_TOKEN found in environment. Please set it.")
    sys.exit(1)

# Bot welcome message
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

# Bot help message
BOT_HELP_MESSAGE = (
    "🔍 *ADHD Buddy Commands*\n\n"
    "• 🌞 /morning - Start your morning ritual\n"
    "• 📝 /habits - Track your habits for today\n"
    "• 🌙 /evening - Evening reflection\n"
    "• 💬 /coach - Get supportive coaching\n"
    "• 📊 /stats - View your progress and streaks\n"
    "• ℹ️ /help - Show this help message\n\n"
    "Remember, consistency is key! Try to check in with me daily."
)

# Create keyboard markup
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
    """Handle the /start command."""
    logger.info(f"User {update.effective_user.id} started the bot")
    
    # Create a keyboard with a Web App button
    webapp_url = "https://85b8367a-20dd-498d-ba2b-54d9658d5a93-00-2r6boeo2pgged.kirk.replit.dev/"
    
    # Create a button with WebAppInfo
    web_app_button = InlineKeyboardButton(
        text="📱 Open Web App",
        web_app=WebAppInfo(url=webapp_url)
    )
    
    # Add the button to a keyboard
    keyboard = [
        [web_app_button],
        [InlineKeyboardButton("🌞 Morning Ritual", callback_data="morning_ritual")],
        [InlineKeyboardButton("🌙 Evening Reflection", callback_data="evening_reflection")],
        [InlineKeyboardButton("📝 Track Habits", callback_data="track_habits")],
        [InlineKeyboardButton("💬 Coach", callback_data="coach")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    
    # Create the reply markup
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the message with the WebApp button
    update.message.reply_text(
        "👋 Welcome to ADHD Support Bot!\n\n"
        "Click the button below to open the web application:",
        reply_markup=reply_markup
    )

def help_command(update: Update, context: CallbackContext) -> None:
    """Handle the /help command."""
    update.message.reply_text(
        BOT_HELP_MESSAGE,
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

def morning_command(update: Update, context: CallbackContext) -> None:
    """Handle the /morning command."""
    update.message.reply_text(
        "Starting the morning ritual. This feature is coming soon!",
        reply_markup=get_main_keyboard()
    )

def habits_command(update: Update, context: CallbackContext) -> None:
    """Handle the /habits command."""
    update.message.reply_text(
        "Here are your habits for today. This feature is coming soon!",
        reply_markup=get_main_keyboard()
    )

def evening_command(update: Update, context: CallbackContext) -> None:
    """Handle the /evening command."""
    update.message.reply_text(
        "Starting the evening reflection. This feature is coming soon!",
        reply_markup=get_main_keyboard()
    )

def coach_command(update: Update, context: CallbackContext) -> None:
    """Handle the /coach command."""
    update.message.reply_text(
        "Ready to chat! This feature is coming soon!",
        reply_markup=get_main_keyboard()
    )

def stats_command(update: Update, context: CallbackContext) -> None:
    """Handle the /stats command."""
    update.message.reply_text(
        "Here are your stats. This feature is coming soon!",
        reply_markup=get_main_keyboard()
    )

def echo(update: Update, context: CallbackContext) -> None:
    """Echo back messages that are not commands."""
    update.message.reply_text(f"You said: {update.message.text}\nTry /help to see available commands.")

def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    query.answer()
    
    if query.data == "help":
        query.edit_message_text(
            text=BOT_HELP_MESSAGE,
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )
    elif query.data == "morning_ritual":
        query.edit_message_text(
            text="Starting the morning ritual. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )
    elif query.data == "evening_reflection":
        query.edit_message_text(
            text="Starting the evening reflection. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )
    elif query.data == "track_habits":
        query.edit_message_text(
            text="Here are your habits for today. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )
    elif query.data == "coach":
        query.edit_message_text(
            text="Ready to chat! This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )
    elif query.data == "stats":
        query.edit_message_text(
            text="Here are your stats. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )
    else:
        query.edit_message_text(
            text=f"You selected {query.data}. This feature is coming soon!",
            reply_markup=get_main_keyboard()
        )

def main():
    """Start the bot."""
    try:
        # Create the updater and pass it the bot's token
        updater = Updater(BOT_TOKEN)
        
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher
        
        # Register command handlers
        dispatcher.add_handler(CommandHandler("start", start_command))
        dispatcher.add_handler(CommandHandler("help", help_command))
        dispatcher.add_handler(CommandHandler("morning", morning_command))
        dispatcher.add_handler(CommandHandler("habits", habits_command))
        dispatcher.add_handler(CommandHandler("evening", evening_command))
        dispatcher.add_handler(CommandHandler("coach", coach_command))
        dispatcher.add_handler(CommandHandler("stats", stats_command))
        
        # Register callback query handler
        dispatcher.add_handler(CallbackQueryHandler(button_callback))
        
        # Register message handler
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
        
        # Start the bot
        logger.info("Starting bot...")
        updater.start_polling()
        logger.info("Bot is polling for updates")
        
        # Run the bot until Ctrl-C is pressed
        updater.idle()
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
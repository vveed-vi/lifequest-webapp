import os
import logging
from flask import Flask, request, jsonify
import telegram
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler, 
    MessageHandler, Filters, ConversationHandler
)

from config import BOT_TOKEN, WEBHOOK_URL
from handlers.command_handlers import (
    start_command, help_command, coach_command, 
    morning_ritual_command, habit_command, 
    evening_reflection_command, stats_command
)
from handlers.callback_handlers import button_callback
from handlers.conversation_handlers import (
    morning_ritual_conversation, evening_reflection_conversation,
    coach_conversation, habit_conversation
)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

# Set default token for development
token = BOT_TOKEN if BOT_TOKEN else "YOUR_TELEGRAM_TOKEN"

# Initialize bot and updater
bot = telegram.Bot(token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher

# Add command handlers
dispatcher.add_handler(CommandHandler("start", start_command))
dispatcher.add_handler(CommandHandler("help", help_command))
dispatcher.add_handler(CommandHandler("coach", coach_command))
dispatcher.add_handler(CommandHandler("morning", morning_ritual_command))
dispatcher.add_handler(CommandHandler("habits", habit_command))
dispatcher.add_handler(CommandHandler("evening", evening_reflection_command))
dispatcher.add_handler(CommandHandler("stats", stats_command))

# Add callback query handler
dispatcher.add_handler(CallbackQueryHandler(button_callback))

# Add conversation handlers
dispatcher.add_handler(morning_ritual_conversation)
dispatcher.add_handler(evening_reflection_conversation)
dispatcher.add_handler(coach_conversation)
dispatcher.add_handler(habit_conversation)

# Flask routes
@app.route('/', methods=['GET'])
def index():
    return "ADHD Support Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming updates from Telegram."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        # Process update in the dispatcher
        dispatcher.process_update(update)
        
        return jsonify({"status": "ok"})

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Set the webhook for the Telegram bot."""
    try:
        webhook_info = bot.get_webhook_info()
        if webhook_info.url != WEBHOOK_URL:
            success = bot.set_webhook(url=WEBHOOK_URL)
            if success:
                return f"Webhook set to {WEBHOOK_URL}"
            else:
                return "Failed to set webhook"
        return f"Webhook already set to {webhook_info.url}"
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return f"Error: {e}"

@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    """Remove the webhook for the Telegram bot."""
    try:
        success = bot.delete_webhook()
        if success:
            return "Webhook removed"
        else:
            return "Failed to remove webhook"
    except Exception as e:
        logger.error(f"Error removing webhook: {e}")
        return f"Error: {e}"

if __name__ == "__main__":
    # Use polling instead of webhook for development
    updater.start_polling()
    logger.info("Bot started polling for updates...")
    
    # Keep the app running
    app.run(host="0.0.0.0", port=5000, debug=True)

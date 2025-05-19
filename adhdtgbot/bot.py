import os
import sys
import logging
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
    ConversationHandler, CallbackContext
)

# Добавляем путь к модулям
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ADHDTelegramHelper')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'services')))


from config import BOT_TOKEN
from handlers.command_handlers import start_command

from handlers.callback_handlers import button_callback
from handlers.conversation_handlers import (
    morning_ritual_conversation, evening_reflection_conversation,
    coach_conversation, habit_conversation
)

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация команд
    dispatcher.add_handler(CommandHandler("start", start_command))

    # Колбэки
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    # Диалоги
    dispatcher.add_handler(morning_ritual_conversation)
    dispatcher.add_handler(evening_reflection_conversation)
    dispatcher.add_handler(coach_conversation)
    dispatcher.add_handler(habit_conversation)

    # Запуск
    updater.start_polling()
    logger.info("✅ Bot is polling for updates...")
    updater.idle()

if __name__ == '__main__':
    main()

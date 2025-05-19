from telegram import Update
from telegram.ext import CallbackContext
from services.user_service import get_or_create_user
import logging

logger = logging.getLogger(__name__)

def start_command(update: Update, context: CallbackContext) -> None:
    """Отправляет только картинку с короткой подписью."""

    user_id = update.effective_user.id
    username = update.effective_user.username or update.effective_user.first_name
    get_or_create_user(user_id, username)

    image_path = '/workspaces/lifequest-webapp/ADHDTelegramHelper/attached_assets/bot_preview.jpg'

    try:
        with open(image_path, "rb") as photo:
            context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=photo,
                caption="✌🏻 Йоу! Чтобы начать, жми кнопку *Открыть приложение*!",
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Ошибка при отправке изображения: {e}")
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="⚠️ Не удалось отправить изображение. Но ты можешь продолжить."
        )

    logger.info(f"User {user_id} started the bot")

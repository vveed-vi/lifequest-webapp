import logging
from telegram import Update
from telegram.ext import CallbackContext
import json

from services.user_service import get_or_create_user, add_xp
from services.habit_service import toggle_habit_completion, get_user_habits
from utils.keyboards import get_habit_tracking_keyboard
from config import XP_HABIT_COMPLETION

logger = logging.getLogger(__name__)

def button_callback(update: Update, context: CallbackContext) -> None:
    """Handle callback queries from inline keyboard buttons."""
    query = update.callback_query
    query.answer()  # Must always answer callback queries
    
    user_id = update.effective_user.id
    
    # Extract the callback data
    data = query.data
    
    # Handle habit toggling
    if data.startswith('habit_'):
        habit_id = int(data.split('_')[1])
        # Toggle the habit completion
        was_completed, habit_name = toggle_habit_completion(user_id, habit_id)
        
        # If the habit was marked as completed (not uncompleted), add XP
        if was_completed:
            add_xp(user_id, XP_HABIT_COMPLETION)
            congratulation_text = f"✅ Completed: {habit_name}\nYou earned {XP_HABIT_COMPLETION} XP!"
        else:
            congratulation_text = f"❌ Uncompleted: {habit_name}"
        
        # Get updated habits and refresh keyboard
        habits = get_user_habits(user_id)
        
        query.edit_message_text(
            f"{congratulation_text}\n\nHere are your habits for today:",
            reply_markup=get_habit_tracking_keyboard(habits, user_id)
        )
    
    # Handle other button types
    elif data == 'refresh_habits':
        habits = get_user_habits(user_id)
        query.edit_message_text(
            "Here are your habits for today. Tap to mark as completed:",
            reply_markup=get_habit_tracking_keyboard(habits, user_id)
        )
    
    elif data == 'main_menu':
        from utils.keyboards import get_main_keyboard
        query.edit_message_text(
            "What would you like to do?",
            reply_markup=get_main_keyboard()
        )
    
    # Start conversations based on callback
    elif data == 'morning_start':
        # This is handled by the ConversationHandler
        pass
    
    elif data == 'evening_start':
        # This is handled by the ConversationHandler
        pass
    
    elif data == 'coach_start':
        # This is handled by the ConversationHandler
        pass
    
    elif data == 'manage_habits':
        # This is handled by the ConversationHandler
        pass
    
    else:
        logger.warning(f"Unhandled callback query: {data}")
        query.edit_message_text(f"Unhandled callback: {data}")

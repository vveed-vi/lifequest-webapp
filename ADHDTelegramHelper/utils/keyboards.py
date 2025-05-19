from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
from typing import List, Dict, Any

def get_main_keyboard() -> InlineKeyboardMarkup:
    """Create the main menu inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("🌞 Morning Ritual", callback_data="morning_start"),
            InlineKeyboardButton("🌙 Evening Reflection", callback_data="evening_start")
        ],
        [
            InlineKeyboardButton("📝 Track Habits", callback_data="refresh_habits"),
            InlineKeyboardButton("📊 View Stats", callback_data="view_stats")
        ],
        [
            InlineKeyboardButton("💬 Coach", callback_data="coach_start"),
            InlineKeyboardButton("⚙️ Manage Habits", callback_data="manage_habits")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_morning_ritual_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for morning ritual."""
    keyboard = [
        [InlineKeyboardButton("Start Morning Ritual", callback_data="morning_start")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_evening_reflection_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for evening reflection."""
    keyboard = [
        [InlineKeyboardButton("Start Evening Reflection", callback_data="evening_start")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_coach_keyboard() -> InlineKeyboardMarkup:
    """Create keyboard for coaching conversation."""
    keyboard = [
        [InlineKeyboardButton("Talk to Coach", callback_data="coach_start")],
        [InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_habit_tracking_keyboard(habits: List[Dict[str, Any]], user_id: int) -> InlineKeyboardMarkup:
    """Create inline keyboard for habit tracking."""
    keyboard = []
    
    for habit in habits:
        # Add checkbox emoji based on completion status
        prefix = "✅ " if habit["completed"] else "⬜ "
        keyboard.append([
            InlineKeyboardButton(
                f"{prefix}{habit['name']}", 
                callback_data=f"habit_{habit['id']}"
            )
        ])
    
    # Add management options
    keyboard.append([
        InlineKeyboardButton("⚙️ Manage Habits", callback_data="manage_habits"),
        InlineKeyboardButton("🔄 Refresh", callback_data="refresh_habits")
    ])
    keyboard.append([InlineKeyboardButton("Back to Main Menu", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_yes_no_keyboard(prefix: str) -> InlineKeyboardMarkup:
    """Create a simple Yes/No keyboard with the given prefix for callback data."""
    keyboard = [
        [
            InlineKeyboardButton("Yes", callback_data=f"{prefix}_yes"),
            InlineKeyboardButton("No", callback_data=f"{prefix}_no")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Create a keyboard with just a cancel button."""
    keyboard = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]
    return InlineKeyboardMarkup(keyboard)

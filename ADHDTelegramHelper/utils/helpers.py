from typing import Dict, Any
from datetime import datetime, timedelta
import random

from utils.constants import get_level_name, EMOJI_STREAK, EMOJI_XP
from services.habit_service import get_habit_completion_percentage

def format_stats(user: Dict[str, Any]) -> str:
    """Format user stats into a readable message."""
    xp = user.get("xp", 0)
    current_streak = user.get("current_streak", 0)
    max_streak = user.get("max_streak", 0)
    
    # Get level based on XP
    level = get_level_name(xp)
    
    # Calculate 7-day habit completion
    user_id = user.get("id")
    habit_percentages = get_habit_completion_percentage(user_id, 7)
    
    # Format the habit completion stats
    habit_stats = ""
    for habit, percentage in habit_percentages.items():
        habit_stats += f"• {habit}: {percentage}%\n"
    
    # Create the stats message
    message = (
        f"*Your Stats* 📊\n\n"
        f"{EMOJI_XP} *XP*: {xp} (Level: {level})\n"
        f"{EMOJI_STREAK} *Current Streak*: {current_streak} days\n"
        f"🏆 *Highest Streak*: {max_streak} days\n\n"
    )
    
    # Add habit completion stats if there are any
    if habit_stats:
        message += f"*7-Day Habit Completion*:\n{habit_stats}\n"
    
    # Add a supportive message
    supportive_messages = [
        "Remember, progress isn't always linear!",
        "Small steps lead to big changes.",
        "Consistency builds neural pathways.",
        "You're doing great, even when it feels hard.",
        "Every completed habit strengthens your executive function."
    ]
    
    message += f"\n💭 *Thought*: _{random.choice(supportive_messages)}_"
    
    return message

def get_greeting() -> str:
    """Return a time-appropriate greeting."""
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def days_since(date_str: str) -> int:
    """Calculate days since a given date string (format: YYYY-MM-DD)."""
    if not date_str:
        return 999  # Large number if no date provided
    
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = today - date
        return delta.days
    except (ValueError, TypeError):
        return 999

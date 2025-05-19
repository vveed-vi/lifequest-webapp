# Button and callback data constants
CALLBACK_MORNING_START = "morning_start"
CALLBACK_EVENING_START = "evening_start"
CALLBACK_COACH_START = "coach_start"
CALLBACK_MANAGE_HABITS = "manage_habits"
CALLBACK_REFRESH_HABITS = "refresh_habits"
CALLBACK_VIEW_STATS = "view_stats"
CALLBACK_MAIN_MENU = "main_menu"
CALLBACK_CANCEL = "cancel"

# Completion status emojis
EMOJI_COMPLETED = "✅"
EMOJI_UNCOMPLETED = "⬜"

# Feature emojis
EMOJI_MORNING = "🌞"
EMOJI_EVENING = "🌙"
EMOJI_HABITS = "📝"
EMOJI_COACH = "💬"
EMOJI_STATS = "📊"
EMOJI_SETTINGS = "⚙️"
EMOJI_STREAK = "🔥"
EMOJI_XP = "⭐"
EMOJI_REFRESH = "🔄"

# Level thresholds
XP_LEVELS = {
    0: "Beginner",
    100: "Regular",
    300: "Consistent",
    600: "Dedicated", 
    1000: "Master of Habits",
    2000: "ADHD Ninja"
}

# Get level name based on XP
def get_level_name(xp: int) -> str:
    """Get the level name for a given amount of XP."""
    level_name = "Beginner"
    for threshold, name in sorted(XP_LEVELS.items()):
        if xp >= threshold:
            level_name = name
        else:
            break
    return level_name

import json
import os
from datetime import datetime
import logging
from typing import Dict, Any, Optional, List, Tuple

# Simple in-memory storage - would be replaced with a database in production
users = {}

# Path for JSON persistence
DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

logger = logging.getLogger(__name__)

def ensure_data_dir_exists():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def load_users_data():
    """Load users data from JSON file."""
    global users
    ensure_data_dir_exists()
    
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r') as f:
                users = json.load(f)
        except Exception as e:
            logger.error(f"Error loading users data: {e}")
            # If there's an error loading, start with empty users
            users = {}
    else:
        users = {}

def save_users_data():
    """Save users data to JSON file."""
    ensure_data_dir_exists()
    
    try:
        with open(USER_DATA_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving users data: {e}")

# Load users data at module import
load_users_data()

def get_or_create_user(user_id: int, username: str = None) -> Dict[str, Any]:
    """Get or create a user record."""
    user_id_str = str(user_id)  # Convert to string for JSON compatibility
    
    if user_id_str not in users:
        # Create new user
        users[user_id_str] = {
            "id": user_id,
            "username": username,
            "created_at": datetime.now().isoformat(),
            "xp": 0,
            "current_streak": 0,
            "max_streak": 0,
            "last_morning_ritual": None,
            "last_evening_reflection": None,
            "habits": [],
            "completed_habits": {},  # Keyed by date
            "morning_ritual_answers": [],
            "evening_reflection_answers": []
        }
        save_users_data()
    
    return users[user_id_str]

def update_user_field(user_id: int, field: str, value: Any) -> None:
    """Update a specific field for a user."""
    user_id_str = str(user_id)
    
    if user_id_str in users:
        users[user_id_str][field] = value
        
        # If updating streak, check if it's a new max
        if field == "current_streak":
            current_streak = value
            max_streak = users[user_id_str].get("max_streak", 0)
            
            if current_streak > max_streak:
                users[user_id_str]["max_streak"] = current_streak
        
        save_users_data()

def add_xp(user_id: int, amount: int) -> int:
    """Add XP to user and return new total."""
    user_id_str = str(user_id)
    
    if user_id_str in users:
        users[user_id_str]["xp"] = users[user_id_str].get("xp", 0) + amount
        save_users_data()
        return users[user_id_str]["xp"]
    
    return 0

def get_user_streak(user_id: int) -> Tuple[int, int]:
    """Get current and max streak for a user."""
    user_id_str = str(user_id)
    
    if user_id_str in users:
        current_streak = users[user_id_str].get("current_streak", 0)
        max_streak = users[user_id_str].get("max_streak", 0)
        return current_streak, max_streak
    
    return 0, 0

def check_streak_milestone(user_id: int) -> Optional[str]:
    """Check if user has reached a streak milestone and return message if so."""
    from config import STREAK_MESSAGES
    
    current_streak, _ = get_user_streak(user_id)
    
    if current_streak in STREAK_MESSAGES:
        return STREAK_MESSAGES[current_streak]
    
    return None

def reset_streak_if_inactive(user_id: int) -> None:
    """Reset streak if user hasn't completed activities in the last day."""
    user_id_str = str(user_id)
    
    if user_id_str in users:
        user = users[user_id_str]
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Check if user completed either morning ritual or evening reflection yesterday
        last_morning = user.get("last_morning_ritual")
        last_evening = user.get("last_evening_reflection")
        
        if (last_morning != yesterday and last_morning != today) and \
           (last_evening != yesterday and last_evening != today):
            # User was inactive, reset streak
            update_user_field(user_id, "current_streak", 0)

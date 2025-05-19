import json
import os
from datetime import datetime
import logging
from typing import Dict, Any, List, Tuple, Optional

from services.user_service import get_or_create_user, update_user_field
from config import DEFAULT_HABITS

logger = logging.getLogger(__name__)

def get_user_habits(user_id: int) -> List[Dict[str, Any]]:
    """Get a user's habits with completion status for today."""
    user = get_or_create_user(user_id)
    
    # If user has no habits, set up default habits
    if not user.get("habits"):
        user["habits"] = [{"name": habit, "created_at": datetime.now().isoformat()} 
                           for habit in DEFAULT_HABITS]
        from services.user_service import save_users_data
        save_users_data()
    
    # Get today's completed habits
    today = datetime.now().strftime("%Y-%m-%d")
    completed_today = user.get("completed_habits", {}).get(today, [])
    
    # Prepare habits with completion status
    habits_with_status = []
    for i, habit in enumerate(user["habits"]):
        habits_with_status.append({
            "id": i,
            "name": habit["name"],
            "completed": i in completed_today
        })
    
    return habits_with_status

def toggle_habit_completion(user_id: int, habit_id: int) -> Tuple[bool, str]:
    """Toggle completion status of a habit for today and return new status and habit name."""
    user = get_or_create_user(user_id)
    
    # Make sure the habit exists
    if habit_id >= len(user.get("habits", [])):
        return False, ""
    
    habit_name = user["habits"][habit_id]["name"]
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize completed_habits for today if it doesn't exist
    if "completed_habits" not in user:
        user["completed_habits"] = {}
    
    if today not in user["completed_habits"]:
        user["completed_habits"][today] = []
    
    # Toggle completion status
    completed = habit_id in user["completed_habits"][today]
    
    if completed:
        # Remove from completed list
        user["completed_habits"][today].remove(habit_id)
        was_completed = False
    else:
        # Add to completed list
        user["completed_habits"][today].append(habit_id)
        was_completed = True
    
    # Save changes
    from services.user_service import save_users_data
    save_users_data()
    
    return was_completed, habit_name

def add_habit(user_id: int, habit_name: str) -> bool:
    """Add a new habit for a user. Return True if added, False if already exists."""
    user = get_or_create_user(user_id)
    
    # Check if habit already exists
    for habit in user.get("habits", []):
        if habit["name"].lower() == habit_name.lower():
            return False
    
    # Add new habit
    if "habits" not in user:
        user["habits"] = []
    
    user["habits"].append({
        "name": habit_name,
        "created_at": datetime.now().isoformat()
    })
    
    # Save changes
    from services.user_service import save_users_data
    save_users_data()
    
    return True

def remove_habit(user_id: int, habit_id: str) -> Optional[str]:
    """Remove a habit for a user. Return the habit name if successfully removed."""
    user = get_or_create_user(user_id)
    
    try:
        habit_id = int(habit_id)
        
        # Make sure the habit exists
        if habit_id >= len(user.get("habits", [])):
            return None
        
        # Get the habit name before removing
        habit_name = user["habits"][habit_id]["name"]
        
        # Remove the habit
        del user["habits"][habit_id]
        
        # Update completed habits to remove references to this habit ID
        # This is complicated because we need to shift habit IDs
        if "completed_habits" in user:
            for date in user["completed_habits"]:
                # Filter out the removed habit ID
                completed = user["completed_habits"][date]
                new_completed = []
                
                for h_id in completed:
                    if h_id < habit_id:
                        # IDs before the removed one stay the same
                        new_completed.append(h_id)
                    elif h_id > habit_id:
                        # IDs after the removed one shift down by 1
                        new_completed.append(h_id - 1)
                
                user["completed_habits"][date] = new_completed
        
        # Save changes
        from services.user_service import save_users_data
        save_users_data()
        
        return habit_name
    except (ValueError, IndexError):
        return None

def get_habit_completion_percentage(user_id: int, days: int = 7) -> Dict[str, float]:
    """Get completion percentage for each habit over the last [days] days."""
    user = get_or_create_user(user_id)
    
    # Get habits
    habits = user.get("habits", [])
    
    # Generate list of dates to check
    today = datetime.now()
    dates = [(today - datetime.timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)]
    
    # Initialize results
    results = {}
    for i, habit in enumerate(habits):
        name = habit["name"]
        completed_count = 0
        
        # Check each date
        for date in dates:
            completed_habits = user.get("completed_habits", {}).get(date, [])
            if i in completed_habits:
                completed_count += 1
        
        # Calculate percentage
        percentage = (completed_count / days) * 100 if days > 0 else 0
        results[name] = round(percentage, 1)
    
    return results

from typing import Dict, List, Any, Optional
from datetime import datetime

class User:
    """User model for ADHD support bot."""
    
    def __init__(
        self, 
        user_id: int, 
        username: str = None,
        xp: int = 0,
        current_streak: int = 0,
        max_streak: int = 0,
        last_morning_ritual: str = None,
        last_evening_reflection: str = None,
        habits: List[Dict[str, Any]] = None,
        completed_habits: Dict[str, List[int]] = None,
        morning_ritual_answers: List[str] = None,
        evening_reflection_answers: List[str] = None,
        created_at: str = None
    ):
        self.user_id = user_id
        self.username = username
        self.xp = xp
        self.current_streak = current_streak
        self.max_streak = max_streak
        self.last_morning_ritual = last_morning_ritual
        self.last_evening_reflection = last_evening_reflection
        self.habits = habits or []
        self.completed_habits = completed_habits or {}
        self.morning_ritual_answers = morning_ritual_answers or []
        self.evening_reflection_answers = evening_reflection_answers or []
        self.created_at = created_at or datetime.now().isoformat()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        """Create a User object from a dictionary."""
        return cls(
            user_id=data.get('id'),
            username=data.get('username'),
            xp=data.get('xp', 0),
            current_streak=data.get('current_streak', 0),
            max_streak=data.get('max_streak', 0),
            last_morning_ritual=data.get('last_morning_ritual'),
            last_evening_reflection=data.get('last_evening_reflection'),
            habits=data.get('habits', []),
            completed_habits=data.get('completed_habits', {}),
            morning_ritual_answers=data.get('morning_ritual_answers', []),
            evening_reflection_answers=data.get('evening_reflection_answers', []),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert User object to a dictionary."""
        return {
            'id': self.user_id,
            'username': self.username,
            'xp': self.xp,
            'current_streak': self.current_streak,
            'max_streak': self.max_streak,
            'last_morning_ritual': self.last_morning_ritual,
            'last_evening_reflection': self.last_evening_reflection,
            'habits': self.habits,
            'completed_habits': self.completed_habits,
            'morning_ritual_answers': self.morning_ritual_answers,
            'evening_reflection_answers': self.evening_reflection_answers,
            'created_at': self.created_at
        }
    
    def has_completed_morning_ritual_today(self) -> bool:
        """Check if user has completed morning ritual today."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.last_morning_ritual == today
    
    def has_completed_evening_reflection_today(self) -> bool:
        """Check if user has completed evening reflection today."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.last_evening_reflection == today
    
    def get_streak_message(self) -> Optional[str]:
        """Get a message based on the user's current streak milestone."""
        from config import STREAK_MESSAGES
        
        if self.current_streak in STREAK_MESSAGES:
            return STREAK_MESSAGES[self.current_streak]
        
        return None
    
    def check_and_reset_streak(self) -> None:
        """Check and reset streak if user didn't complete activities yesterday."""
        today = datetime.now()
        yesterday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        # If user did neither morning nor evening reflection yesterday, reset streak
        if (self.last_morning_ritual != yesterday and 
            self.last_evening_reflection != yesterday):
            self.current_streak = 0

from typing import Dict, List, Any, Optional
from datetime import datetime

class Habit:
    """Habit model for ADHD support bot."""
    
    def __init__(
        self,
        name: str,
        created_at: str = None,
        id: Optional[int] = None
    ):
        self.name = name
        self.created_at = created_at or datetime.now().isoformat()
        self.id = id
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any], id: Optional[int] = None) -> 'Habit':
        """Create a Habit object from a dictionary."""
        return cls(
            name=data.get('name'),
            created_at=data.get('created_at'),
            id=id
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert Habit object to a dictionary."""
        return {
            'name': self.name,
            'created_at': self.created_at
        }

class HabitCompletion:
    """Record of habit completion."""
    
    def __init__(
        self,
        habit_id: int,
        completed_at: str = None
    ):
        self.habit_id = habit_id
        self.completed_at = completed_at or datetime.now().isoformat()
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HabitCompletion':
        """Create a HabitCompletion object from a dictionary."""
        return cls(
            habit_id=data.get('habit_id'),
            completed_at=data.get('completed_at')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert HabitCompletion object to a dictionary."""
        return {
            'habit_id': self.habit_id,
            'completed_at': self.completed_at
        }

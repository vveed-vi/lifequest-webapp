import random
import logging
from typing import List, Dict, Any, Optional

from config import SUPPORTIVE_RESPONSES

logger = logging.getLogger(__name__)

# Simple coaching responses based on keywords
COACHING_RESPONSES = {
    "focus": [
        "For focus challenges, try the Pomodoro technique: 25 minutes of focus followed by a 5-minute break.",
        "Creating a dedicated workspace with minimal distractions can help with focus.",
        "Sometimes, background noise like lo-fi music or nature sounds can help with focus.",
        "Try using a 'body double' - work alongside someone else (even virtually) for accountability.",
        "Consider breaking down tasks into smaller, more manageable pieces to improve focus."
    ],
    "procrastination": [
        "Procrastination happens to everyone with ADHD. Try starting with just 5 minutes on the task.",
        "The 'two-minute rule' can help - if a task takes less than two minutes, do it right away.",
        "External accountability can help - tell someone about your deadline or work with a buddy.",
        "Reward yourself for starting tasks, not just completing them.",
        "Sometimes procrastination is about perfectionism - remember that done is better than perfect."
    ],
    "overwhelm": [
        "When you're feeling overwhelmed, try a brain dump - write everything down without organizing at first.",
        "For overwhelm, the 1-3-5 rule can help: plan to accomplish 1 big thing, 3 medium things, and 5 small things.",
        "Remember that it's okay to say no to new commitments when you're feeling overwhelmed.",
        "Break large projects into specific, concrete next steps - focus on just the next action.",
        "Try the 'Swiss cheese' method - poke holes in big tasks by doing small parts whenever you can."
    ],
    "forget": [
        "External reminders like alarms, sticky notes, or apps can help with forgetfulness.",
        "Try creating routines and attaching new habits to existing ones to help remember.",
        "Visual cues in your environment can help - like putting items you need by the door.",
        "Digital calendar reminders with multiple alerts can help with time-based responsibilities.",
        "Consider using a task manager app that sends notifications for important tasks."
    ],
    "motivation": [
        "For motivation struggles, try body doubling - work alongside someone else doing their own work.",
        "Sometimes music can jumpstart motivation - try creating a 'get started' playlist.",
        "Motivation often follows action - start with just 5 minutes and see if it builds.",
        "Gamifying tasks can help with motivation - set timers and try to 'beat the clock'.",
        "Build in immediate rewards for completing difficult tasks to boost motivation."
    ],
    "time": [
        "Time blindness is common with ADHD. Try using visual timers to make time more concrete.",
        "Scheduling buffer time between activities can help with time management challenges.",
        "The 'time multiplier' rule can help - estimate how long a task will take, then multiply by 1.5.",
        "Setting alarms not just for start times but also for transition times can help with time awareness.",
        "Consider time-tracking for a week to gain insight into where your time actually goes."
    ],
    "sleep": [
        "A consistent sleep schedule helps ADHD symptoms - try to go to bed and wake up at the same times.",
        "Reducing screen time 1-2 hours before bed can help with sleep quality.",
        "Creating a wind-down routine signals to your brain that it's time for sleep.",
        "Consider using a white noise machine or app if your mind races at night.",
        "Exercising during the day (but not right before bed) can help with sleep quality."
    ],
    "emotion": [
        "Emotional regulation can be challenging with ADHD. Deep breathing exercises can help in the moment.",
        "Naming your emotions specifically can help reduce their intensity.",
        "Building in transition time between activities can reduce emotional overload.",
        "Regular exercise has been shown to help with emotional regulation.",
        "Remember that rejection sensitive dysphoria is common with ADHD - your feelings are valid."
    ],
    "organization": [
        "For organization, try the 'everything has a home' rule - designate specific spots for important items.",
        "Visual organization systems often work better than hidden storage for ADHD brains.",
        "Digital organization tools like cloud storage and search functions can help compensate for ADHD challenges.",
        "Consider using color-coding for different categories of items or information.",
        "Regular 'reset' sessions (daily or weekly) can help maintain organization systems."
    ],
    "medication": [
        "Medication works differently for everyone. It's important to work closely with your healthcare provider.",
        "Keeping a symptom journal can help track medication effectiveness.",
        "Remember that medication is a tool, not a complete solution - strategies and skills are still important.",
        "If you're having side effects, don't give up - talk to your doctor about adjustments.",
        "Some people find that medication needs change with different contexts or life phases."
    ]
}

# Default responses for when no keywords are matched
DEFAULT_RESPONSES = [
    "That sounds challenging. What strategies have you tried so far?",
    "I hear you. Let's think about a small step you could take toward addressing that.",
    "That's a common ADHD experience. Would it help to break this down into smaller pieces?",
    "Your feelings are valid. Is there a specific part of this situation you'd like to focus on?",
    "Remember to be kind to yourself - ADHD makes some things genuinely harder.",
    "Would it help to think about what advice you'd give a friend in this situation?",
    "Sometimes just acknowledging the challenge is an important first step.",
    "That's something many people with ADHD experience. You're not alone in this."
]

def get_coaching_response(user_message: str) -> str:
    """Generate a coaching response based on the user's message."""
    user_message = user_message.lower()
    
    # Check for keywords in the user's message
    for keyword, responses in COACHING_RESPONSES.items():
        if keyword in user_message:
            return random.choice(responses)
    
    # If no keywords matched, return a default response
    return random.choice(DEFAULT_RESPONSES + SUPPORTIVE_RESPONSES)

def get_coaching_prompt() -> str:
    """Get a random coaching prompt to start a conversation."""
    from config import COACH_PROMPTS
    return random.choice(COACH_PROMPTS)

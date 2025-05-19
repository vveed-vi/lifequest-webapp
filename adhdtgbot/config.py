import os
from dotenv import load_dotenv
load_dotenv()


# Bot configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL", "https://your-app-url.com/webhook")

# Bot personality and messaging
BOT_NAME = "ADHD Buddy"
BOT_WELCOME_MESSAGE = (
    "👋 Hello! I'm your ADHD support buddy. I'm here to help you establish routines, "
    "track habits, and provide support when you need it.\n\n"
    "Here's what I can do:\n"
    "• 🌞 /morning - Start your day with a morning ritual\n"
    "• 📝 /habits - Track your daily habits\n"
    "• 🌙 /evening - Reflect on your day\n"
    "• 💬 /coach - Chat with me for support and advice\n"
    "• 📊 /stats - View your progress and streaks\n"
    "• ℹ️ /help - See all available commands\n\n"
    "Let's make today a great day!"
)

BOT_HELP_MESSAGE = (
    "🔍 *ADHD Buddy Commands*\n\n"
    "• 🌞 /morning - Start your morning ritual\n"
    "• 📝 /habits - Track your habits for today\n"
    "• 🌙 /evening - Evening reflection\n"
    "• 💬 /coach - Get supportive coaching\n"
    "• 📊 /stats - View your streaks and XP\n"
    "• ℹ️ /help - Show this help message\n\n"
    "Remember, consistency is key! Try to check in with me daily."
)

# XP System
XP_MORNING_RITUAL = 10
XP_HABIT_COMPLETION = 5
XP_EVENING_REFLECTION = 10
XP_COACH_INTERACTION = 2

# Default habits
DEFAULT_HABITS = [
    "Take medications",
    "Drink water",
    "Exercise",
    "Meditation/mindfulness",
    "Plan/review tasks"
]

# Coach conversation prompts
COACH_PROMPTS = [
    "What's been challenging today?",
    "Is there something I can help you with?",
    "What's one small win you've had recently?",
    "Is there a task you're avoiding that we should break down?",
    "What would make today feel successful for you?",
    "Is there a habit you're struggling with that we could modify?"
]

# Morning ritual questions
MORNING_QUESTIONS = [
    "How did you sleep last night?",
    "What's your energy level right now (1-10)?",
    "What's one important task to focus on today?",
    "Is there anything you're worried about today?",
    "What's one small thing you can do for self-care today?"
]

# Evening reflection questions
EVENING_QUESTIONS = [
    "How was your day overall (1-10)?",
    "What's one thing that went well today?",
    "Did you accomplish what you wanted to?",
    "What's one thing you could improve tomorrow?",
    "What are you grateful for today?"
]

# Supportive responses
SUPPORTIVE_RESPONSES = [
    "You're doing great, even when it feels hard.",
    "Remember, progress isn't always linear.",
    "Small steps still move you forward.",
    "I believe in you, even on the tough days.",
    "It's okay to struggle sometimes. You've got this.",
    "Your effort matters, even when results aren't immediate.",
    "Remember to be as kind to yourself as you would be to a friend."
]

# Encouragement messages
STREAK_MESSAGES = {
    3: "🎉 Three day streak! You're building momentum!",
    7: "🔥 One week streak! Excellent consistency!",
    14: "⭐ Two week streak! Your habits are getting stronger!",
    30: "🏆 Thirty day streak! You're amazing!"
}

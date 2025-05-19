import logging
from telegram import Update
from telegram.ext import (
    CallbackContext, ConversationHandler, CommandHandler,
    MessageHandler, Filters, CallbackQueryHandler
)
from datetime import datetime
import random

from adhdtgbot.config import (
    MORNING_QUESTIONS, EVENING_QUESTIONS,
    COACH_PROMPTS, SUPPORTIVE_RESPONSES,
    XP_MORNING_RITUAL, XP_EVENING_REFLECTION,
    XP_COACH_INTERACTION
)
from utils.keyboards import (
    get_main_keyboard, get_morning_ritual_keyboard,
    get_evening_reflection_keyboard, get_coach_keyboard,
    get_yes_no_keyboard
)
from services.user_service import get_or_create_user, add_xp, update_user_field
from services.coach_service import get_coaching_response

logger = logging.getLogger(__name__)

# States for the morning ritual conversation
(
    MORNING_START,
    MORNING_Q1, MORNING_Q2, MORNING_Q3, MORNING_Q4, MORNING_Q5,
    MORNING_END
) = range(7)

# States for the evening reflection conversation
(
    EVENING_START,
    EVENING_Q1, EVENING_Q2, EVENING_Q3, EVENING_Q4, EVENING_Q5,
    EVENING_END
) = range(7)

# States for the coach conversation
(
    COACH_START,
    COACH_RESPONSE,
    COACH_END
) = range(3)

# States for the habit conversation
(
    HABIT_START,
    HABIT_ADD,
    HABIT_REMOVE,
    HABIT_END
) = range(4)

# Morning ritual conversation
def morning_start(update: Update, context: CallbackContext) -> int:
    """Start the morning ritual conversation."""
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            f"Great! Let's start your morning ritual.\n\n"
            f"Question 1: {MORNING_QUESTIONS[0]}"
        )
    else:
        update.message.reply_text(
            f"Great! Let's start your morning ritual.\n\n"
            f"Question 1: {MORNING_QUESTIONS[0]}"
        )
    
    # Initialize context data for storing answers
    context.user_data['morning_answers'] = []
    return MORNING_Q1

def morning_q1(update: Update, context: CallbackContext) -> int:
    """Handle the response to the first morning question and ask the second."""
    answer = update.message.text
    context.user_data['morning_answers'].append(answer)
    
    update.message.reply_text(
        f"Thanks! Question 2: {MORNING_QUESTIONS[1]}"
    )
    return MORNING_Q2

def morning_q2(update: Update, context: CallbackContext) -> int:
    """Handle the response to the second morning question and ask the third."""
    answer = update.message.text
    context.user_data['morning_answers'].append(answer)
    
    update.message.reply_text(
        f"Great! Question 3: {MORNING_QUESTIONS[2]}"
    )
    return MORNING_Q3

def morning_q3(update: Update, context: CallbackContext) -> int:
    """Handle the response to the third morning question and ask the fourth."""
    answer = update.message.text
    context.user_data['morning_answers'].append(answer)
    
    update.message.reply_text(
        f"You're doing great! Question 4: {MORNING_QUESTIONS[3]}"
    )
    return MORNING_Q4

def morning_q4(update: Update, context: CallbackContext) -> int:
    """Handle the response to the fourth morning question and ask the final one."""
    answer = update.message.text
    context.user_data['morning_answers'].append(answer)
    
    update.message.reply_text(
        f"Almost done! Final question: {MORNING_QUESTIONS[4]}"
    )
    return MORNING_Q5

def morning_q5(update: Update, context: CallbackContext) -> int:
    """Handle the response to the fifth morning question and conclude the ritual."""
    answer = update.message.text
    context.user_data['morning_answers'].append(answer)
    
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)
    
    # Update user's morning ritual completion
    today = datetime.now().strftime("%Y-%m-%d")
    update_user_field(user_id, "last_morning_ritual", today)
    
    # Store answers in user data (simplified - in a real app, store in database)
    update_user_field(user_id, "morning_ritual_answers", context.user_data['morning_answers'])
    
    # Add XP and update streak if first time today
    if user.get("last_morning_ritual") != today:
        add_xp(user_id, XP_MORNING_RITUAL)
        update_user_field(user_id, "current_streak", user.get("current_streak", 0) + 1)
    
    # Generate a supportive response
    supportive_msg = random.choice(SUPPORTIVE_RESPONSES)
    
    update.message.reply_text(
        f"✅ Morning ritual complete! You earned {XP_MORNING_RITUAL} XP!\n\n"
        f"{supportive_msg}\n\n"
        "Have a productive day! Remember to check your habits later.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

def morning_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the morning ritual conversation."""
    update.message.reply_text(
        "Morning ritual cancelled. You can restart anytime with /morning.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# Evening reflection conversation
def evening_start(update: Update, context: CallbackContext) -> int:
    """Start the evening reflection conversation."""
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            f"Let's reflect on your day.\n\n"
            f"Question 1: {EVENING_QUESTIONS[0]}"
        )
    else:
        update.message.reply_text(
            f"Let's reflect on your day.\n\n"
            f"Question 1: {EVENING_QUESTIONS[0]}"
        )
    
    # Initialize context data for storing answers
    context.user_data['evening_answers'] = []
    return EVENING_Q1

def evening_q1(update: Update, context: CallbackContext) -> int:
    """Handle the response to the first evening question and ask the second."""
    answer = update.message.text
    context.user_data['evening_answers'].append(answer)
    
    update.message.reply_text(
        f"Thanks! Question 2: {EVENING_QUESTIONS[1]}"
    )
    return EVENING_Q2

def evening_q2(update: Update, context: CallbackContext) -> int:
    """Handle the response to the second evening question and ask the third."""
    answer = update.message.text
    context.user_data['evening_answers'].append(answer)
    
    update.message.reply_text(
        f"Great! Question 3: {EVENING_QUESTIONS[2]}"
    )
    return EVENING_Q3

def evening_q3(update: Update, context: CallbackContext) -> int:
    """Handle the response to the third evening question and ask the fourth."""
    answer = update.message.text
    context.user_data['evening_answers'].append(answer)
    
    update.message.reply_text(
        f"You're doing great! Question 4: {EVENING_QUESTIONS[3]}"
    )
    return EVENING_Q4

def evening_q4(update: Update, context: CallbackContext) -> int:
    """Handle the response to the fourth evening question and ask the final one."""
    answer = update.message.text
    context.user_data['evening_answers'].append(answer)
    
    update.message.reply_text(
        f"Almost done! Final question: {EVENING_QUESTIONS[4]}"
    )
    return EVENING_Q5

def evening_q5(update: Update, context: CallbackContext) -> int:
    """Handle the response to the fifth evening question and conclude the reflection."""
    answer = update.message.text
    context.user_data['evening_answers'].append(answer)
    
    user_id = update.effective_user.id
    user = get_or_create_user(user_id)
    
    # Update user's evening reflection completion
    today = datetime.now().strftime("%Y-%m-%d")
    update_user_field(user_id, "last_evening_reflection", today)
    
    # Store answers in user data (simplified - in a real app, store in database)
    update_user_field(user_id, "evening_reflection_answers", context.user_data['evening_answers'])
    
    # Add XP if first time today
    if user.get("last_evening_reflection") != today:
        add_xp(user_id, XP_EVENING_REFLECTION)
    
    # Generate a supportive response
    supportive_msg = random.choice(SUPPORTIVE_RESPONSES)
    
    update.message.reply_text(
        f"✅ Evening reflection complete! You earned {XP_EVENING_REFLECTION} XP!\n\n"
        f"{supportive_msg}\n\n"
        "Rest well and we'll continue tomorrow!",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

def evening_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the evening reflection conversation."""
    update.message.reply_text(
        "Evening reflection cancelled. You can restart anytime with /evening.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# Coach conversation
def coach_start(update: Update, context: CallbackContext) -> int:
    """Start the coaching conversation."""
    query = update.callback_query
    user_id = update.effective_user.id
    
    # Select a random coaching prompt
    coach_prompt = random.choice(COACH_PROMPTS)
    
    if query:
        query.answer()
        query.edit_message_text(
            f"I'm here to help you. {coach_prompt}"
        )
    else:
        update.message.reply_text(
            f"I'm here to help you. {coach_prompt}"
        )
    
    return COACH_RESPONSE

def coach_respond(update: Update, context: CallbackContext) -> int:
    """Respond to the user's message in the coaching conversation."""
    user_id = update.effective_user.id
    user_message = update.message.text
    
    # Get a coaching response based on the user's message
    response = get_coaching_response(user_message)
    
    # Add XP for engaging with the coach
    add_xp(user_id, XP_COACH_INTERACTION)
    
    # Ask if they want to continue talking
    update.message.reply_text(
        f"{response}\n\nWould you like to continue our conversation?",
        reply_markup=get_yes_no_keyboard('coach_continue')
    )
    
    return COACH_END

def coach_end(update: Update, context: CallbackContext) -> int:
    """End the coaching conversation or continue based on user choice."""
    query = update.callback_query
    query.answer()
    
    if query.data == 'coach_continue_yes':
        # Continue the coaching conversation
        coach_prompt = random.choice(COACH_PROMPTS)
        query.edit_message_text(
            f"Great! Let's keep talking. {coach_prompt}"
        )
        return COACH_RESPONSE
    else:
        # End the coaching conversation
        query.edit_message_text(
            "Thanks for chatting! Remember, I'm here anytime you need support. "
            "Use /coach to start another conversation.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END

def coach_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the coaching conversation."""
    update.message.reply_text(
        "Coaching conversation ended. You can chat anytime with /coach.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# Habit conversation
def habit_start(update: Update, context: CallbackContext) -> int:
    """Start the habit management conversation."""
    query = update.callback_query
    if query:
        query.answer()
        query.edit_message_text(
            "Would you like to add a new habit or remove an existing one?",
            reply_markup=get_habit_management_keyboard()
        )
    else:
        update.message.reply_text(
            "Would you like to add a new habit or remove an existing one?",
            reply_markup=get_habit_management_keyboard()
        )
    return HABIT_START

def habit_add(update: Update, context: CallbackContext) -> int:
    """Handle adding a new habit."""
    query = update.callback_query
    query.answer()
    
    query.edit_message_text(
        "Please send me the name of the habit you want to add:"
    )
    return HABIT_ADD

def habit_handle_add(update: Update, context: CallbackContext) -> int:
    """Process the new habit name."""
    habit_name = update.message.text
    user_id = update.effective_user.id
    
    # Add the habit using the habit service
    from services.habit_service import add_habit
    success = add_habit(user_id, habit_name)
    
    if success:
        update.message.reply_text(
            f"✅ Added new habit: {habit_name}\n\n"
            "Would you like to add another habit?",
            reply_markup=get_yes_no_keyboard('add_another_habit')
        )
    else:
        update.message.reply_text(
            f"That habit already exists in your list.\n\n"
            "Would you like to add a different habit?",
            reply_markup=get_yes_no_keyboard('add_another_habit')
        )
    
    return HABIT_END

def habit_remove(update: Update, context: CallbackContext) -> int:
    """Handle removing an existing habit."""
    query = update.callback_query
    query.answer()
    
    user_id = update.effective_user.id
    from services.habit_service import get_user_habits
    habits = get_user_habits(user_id)
    
    if not habits:
        query.edit_message_text(
            "You don't have any habits to remove.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END
    
    query.edit_message_text(
        "Which habit would you like to remove?",
        reply_markup=get_habit_removal_keyboard(habits)
    )
    return HABIT_REMOVE

def habit_handle_remove(update: Update, context: CallbackContext) -> int:
    """Process the habit removal."""
    query = update.callback_query
    query.answer()
    
    habit_id = query.data.split('_')[-1]
    user_id = update.effective_user.id
    
    # Remove the habit using the habit service
    from services.habit_service import remove_habit
    habit_name = remove_habit(user_id, habit_id)
    
    if habit_name:
        query.edit_message_text(
            f"✅ Removed habit: {habit_name}\n\n"
            "Would you like to remove another habit?",
            reply_markup=get_yes_no_keyboard('remove_another_habit')
        )
    else:
        query.edit_message_text(
            "Could not find that habit.\n\n"
            "Would you like to try again?",
            reply_markup=get_yes_no_keyboard('remove_another_habit')
        )
    
    return HABIT_END

def habit_end(update: Update, context: CallbackContext) -> int:
    """End the habit management conversation or continue based on user choice."""
    query = update.callback_query
    query.answer()
    
    if query.data == 'add_another_habit_yes' or query.data == 'remove_another_habit_yes':
        # Redirect back to start of habit management
        query.edit_message_text(
            "Would you like to add a new habit or remove an existing one?",
            reply_markup=get_habit_management_keyboard()
        )
        return HABIT_START
    else:
        # End the habit management
        query.edit_message_text(
            "Habit management completed. Use /habits to track your daily habits.",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END

def habit_cancel(update: Update, context: CallbackContext) -> int:
    """Cancel the habit management conversation."""
    update.message.reply_text(
        "Habit management cancelled. Use /habits to track your daily habits.",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

# Create conversation handlers
morning_ritual_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("morning", morning_start),
        CallbackQueryHandler(morning_start, pattern='^morning_start$')
    ],
    states={
        MORNING_START: [MessageHandler(Filters.text & ~Filters.command, morning_q1)],
        MORNING_Q1: [MessageHandler(Filters.text & ~Filters.command, morning_q2)],
        MORNING_Q2: [MessageHandler(Filters.text & ~Filters.command, morning_q3)],
        MORNING_Q3: [MessageHandler(Filters.text & ~Filters.command, morning_q4)],
        MORNING_Q4: [MessageHandler(Filters.text & ~Filters.command, morning_q5)],
        MORNING_Q5: [MessageHandler(Filters.text & ~Filters.command, morning_q5)],
    },
    fallbacks=[CommandHandler("cancel", morning_cancel)],
)

evening_reflection_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("evening", evening_start),
        CallbackQueryHandler(evening_start, pattern='^evening_start$')
    ],
    states={
        EVENING_START: [MessageHandler(Filters.text & ~Filters.command, evening_q1)],
        EVENING_Q1: [MessageHandler(Filters.text & ~Filters.command, evening_q2)],
        EVENING_Q2: [MessageHandler(Filters.text & ~Filters.command, evening_q3)],
        EVENING_Q3: [MessageHandler(Filters.text & ~Filters.command, evening_q4)],
        EVENING_Q4: [MessageHandler(Filters.text & ~Filters.command, evening_q5)],
        EVENING_Q5: [MessageHandler(Filters.text & ~Filters.command, evening_q5)],
    },
    fallbacks=[CommandHandler("cancel", evening_cancel)],
)

coach_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("coach", coach_start),
        CallbackQueryHandler(coach_start, pattern='^coach_start$')
    ],
    states={
        COACH_START: [MessageHandler(Filters.text & ~Filters.command, coach_respond)],
        COACH_RESPONSE: [MessageHandler(Filters.text & ~Filters.command, coach_respond)],
        COACH_END: [
            CallbackQueryHandler(coach_end, pattern='^coach_continue_')
        ],
    },
    fallbacks=[CommandHandler("cancel", coach_cancel)],
)

habit_conversation = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(habit_start, pattern='^manage_habits$')
    ],
    states={
        HABIT_START: [
            CallbackQueryHandler(habit_add, pattern='^add_habit$'),
            CallbackQueryHandler(habit_remove, pattern='^remove_habit$')
        ],
        HABIT_ADD: [MessageHandler(Filters.text & ~Filters.command, habit_handle_add)],
        HABIT_REMOVE: [CallbackQueryHandler(habit_handle_remove, pattern='^remove_habit_')],
        HABIT_END: [
            CallbackQueryHandler(habit_end, pattern='^add_another_habit_'),
            CallbackQueryHandler(habit_end, pattern='^remove_another_habit_')
        ],
    },
    fallbacks=[CommandHandler("cancel", habit_cancel)],
)

# Helper functions for habit conversation
def get_habit_management_keyboard():
    """Create inline keyboard for habit management options."""
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = [
        [
            InlineKeyboardButton("Add Habit", callback_data="add_habit"),
            InlineKeyboardButton("Remove Habit", callback_data="remove_habit")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_habit_removal_keyboard(habits):
    """Create inline keyboard for habit removal."""
    from telegram import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = []
    
    for i, habit in enumerate(habits):
        keyboard.append([InlineKeyboardButton(habit, callback_data=f"remove_habit_{i}")])
    
    keyboard.append([InlineKeyboardButton("Cancel", callback_data="cancel_habit_removal")])
    
    return InlineKeyboardMarkup(keyboard)

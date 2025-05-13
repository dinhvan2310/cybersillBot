from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from services.lang_service import get_text
from controllers.user_controller import handle_register_user
from services.user_service import update_user_language
import asyncio

async def send_main_menu(message_or_query, lang):
    keyboard = [
        [InlineKeyboardButton(get_text("buy_code", lang), callback_data='buy')],
        [
            InlineKeyboardButton(get_text("check_transaction", lang), callback_data='check_transaction'),
            InlineKeyboardButton(get_text("support", lang), callback_data='support')
        ],
        [InlineKeyboardButton(get_text("choose_language", lang), callback_data='choose_language')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = get_text("choose_function", lang)
    if hasattr(message_or_query, "edit_message_text"):
        await message_or_query.edit_message_text(text, reply_markup=reply_markup)
    else:
        await message_or_query.reply_text(text, reply_markup=reply_markup)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tg_user = update.effective_user
    user = handle_register_user(tg_user.id, tg_user.username, getattr(tg_user, 'email', None))
    lang = getattr(user, 'language', 'en')
    await update.message.reply_text (
        get_text("welcome", lang)
    )
    await send_main_menu(update.message, lang)

# Handler cho các callback_data của menu chính
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    lang = 'en'
    await query.answer()
    if query.data == 'buy':
        await query.edit_message_text(get_text("buy_code", lang) + ": Coming soon!")
    elif query.data == 'check_transaction':
        await query.edit_message_text(get_text("check_transaction", lang) + ": Coming soon!")
    elif query.data == 'support':
        await query.edit_message_text(get_text("support", lang) + ": Coming soon!")
    elif query.data == 'choose_language':
        keyboard = [
            [
                InlineKeyboardButton("🇻🇳 Tiếng Việt", callback_data='set_lang_vi'),
                InlineKeyboardButton("🇺🇸 English", callback_data='set_lang_en')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(get_text("choose_language", lang), reply_markup=reply_markup)
    elif query.data == 'set_lang_vi':
        update_user_language(user.id, 'vi')
        await query.edit_message_text(get_text("language_changed", 'vi', language="Tiếng Việt"))
        await asyncio.sleep(2)
        await send_main_menu(query, 'vi')
    elif query.data == 'set_lang_en':
        update_user_language(user.id, 'en')
        await query.edit_message_text(get_text("language_changed", 'en', language="English"))
        await asyncio.sleep(2)
        await send_main_menu(query, 'en')
    else:
        await query.edit_message_text("Unknown action.")
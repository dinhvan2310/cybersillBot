from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler, ConversationHandler, MessageHandler, filters
from services.lang_service import get_text
from controllers.user_controller import handle_register_user
from services.user_service import update_user_language, get_user_by_telegram_id, update_user_balance
from services.payment_service import create_invoice
from services.transaction_service import get_transactions_by_user, add_transaction, update_transaction_status
import asyncio
import config
import os

DEPOSIT_AMOUNT = 1001

async def send_main_menu(message_or_query, lang=None):
    user_id = None
    if hasattr(message_or_query, 'from_user'):
        user_id = message_or_query.from_user.id
    elif hasattr(message_or_query, 'chat'):
        user_id = message_or_query.chat.id
    if user_id:
        user_obj = get_user_by_telegram_id(user_id)
        lang = getattr(user_obj, 'language', lang or 'en') if user_obj else (lang or 'en')
    else:
        lang = lang or 'en'
    keyboard = [
        [InlineKeyboardButton(f"{get_text('buy_code', lang)} ({config.PRICE_PER_CODE} USDT)", callback_data='buy')],
        [InlineKeyboardButton(get_text("deposit", lang), callback_data='deposit')],
        [InlineKeyboardButton(get_text("view_balance", lang), callback_data='view_balance')],
        [
            InlineKeyboardButton(get_text("check_transaction", lang), callback_data='check_transaction'),
            InlineKeyboardButton(get_text("support", lang), callback_data='support')
        ],
        [InlineKeyboardButton(get_text("join_group", lang), url="https://web.telegram.org/k/#-4985701255")],
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
    lang = getattr(user, 'language', 'en') if user else 'en'
    await update.message.reply_text(get_text("welcome", lang))
    await send_main_menu(update.message, lang)

# Handler cho các callback_data của menu chính
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    user_obj = get_user_by_telegram_id(user.id)
    lang = getattr(user_obj, 'language', 'en') if user_obj else 'en'
    await query.answer()
    if query.data == 'buy':
        balance = getattr(user_obj, 'balance', 0.0) if user_obj else 0.0
        price = config.PRICE_PER_CODE
        if balance >= price:
            update_user_balance(user.id, balance - price)
            add_transaction(user.id, 'purchase', price, 'success', description=None)
            await query.edit_message_text(get_text("send_code_success", lang))
            file_path = "product/source_code.zip"
            try:
                with open(file_path, "rb") as f:
                    await context.bot.send_document(
                        chat_id=user.id,
                        document=f,
                        caption=get_text("send_code_caption", lang),
                    )
            except Exception as e:
                await context.bot.send_message(chat_id=user.id, text=get_text("send_code_error", lang) + f" {e}")
        else:
            await query.edit_message_text(get_text("not_enough_balance", lang).format(price=price, balance=balance))
    elif query.data == 'check_transaction':
        transactions = get_transactions_by_user(user.id)
        if not transactions:
            await query.edit_message_text(get_text("no_transaction", lang))
        else:
            lines = [get_text("transaction_history_title", lang)]
            for t in transactions:
                type_text = get_text(f"transaction_{t.type}", lang) if t.type in ["deposit", "purchase"] else t.type
                lines.append(get_text("transaction_item", lang).format(
                    type=type_text,
                    amount=t.amount,
                    status=t.status,
                    time=t.created_at.split("T")[0],
                    desc=t.description or ""
                ))
            await query.edit_message_text("\n".join(lines))
    elif query.data == 'support':
        # Đọc file markdown hỗ trợ đúng ngôn ngữ
        support_file = f"i18n/support_{lang}.md"
        if not os.path.exists(support_file):
            support_file = "i18n/support_en.md"
        with open(support_file, "r", encoding="utf-8") as f:
            support_text = f.read()
        await query.edit_message_text(support_text, parse_mode=None, disable_web_page_preview=True)
    elif query.data == 'choose_language':
        keyboard = [
            [
                InlineKeyboardButton("🇻🇳 Tiếng Việt", callback_data='set_lang_vi'),
                InlineKeyboardButton("🇺🇸 English", callback_data='set_lang_en'),
                InlineKeyboardButton("🇨🇳 中文", callback_data='set_lang_zh'),
                InlineKeyboardButton("🇷🇺 Русский", callback_data='set_lang_ru'),
                InlineKeyboardButton("🇯🇵 日本語", callback_data='set_lang_ja')
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
    elif query.data == 'set_lang_zh':
        update_user_language(user.id, 'zh')
        await query.edit_message_text(get_text("language_changed", 'zh', language="中文"))
        await asyncio.sleep(2)
        await send_main_menu(query, 'zh')
    elif query.data == 'set_lang_ru':
        update_user_language(user.id, 'ru')
        await query.edit_message_text(get_text("language_changed", 'ru', language="Русский"))
        await asyncio.sleep(2)
        await send_main_menu(query, 'ru')
    elif query.data == 'set_lang_ja':
        update_user_language(user.id, 'ja')
        await query.edit_message_text(get_text("language_changed", 'ja', language="日本語"))
        await asyncio.sleep(2)
        await send_main_menu(query, 'ja')
    elif query.data == 'deposit':
        await deposit_start(update, context)
    elif query.data == 'view_balance':
        balance = getattr(user_obj, 'balance', 0.0) if user_obj else 0.0
        await query.edit_message_text(get_text("your_balance", lang).format(balance=balance))
    else:
        await query.edit_message_text("Unknown action.")

async def deposit_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_obj = get_user_by_telegram_id(user_id)
    lang = getattr(user_obj, 'language', 'en') if user_obj else 'en'
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(get_text("ask_deposit_amount", lang))
    return DEPOSIT_AMOUNT

async def deposit_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_obj = get_user_by_telegram_id(user_id)
    lang = getattr(user_obj, 'language', 'en') if user_obj else 'en'
    try:
        amount = float(update.message.text.strip())
        print("amount: ", amount)
        if amount < 1:
            await update.message.reply_text(get_text("invalid_deposit_amount", lang))
            return DEPOSIT_AMOUNT
    except Exception:
        await update.message.reply_text(get_text("invalid_deposit_amount", lang))
        return DEPOSIT_AMOUNT
    # Tạo giao dịch nạp tiền trạng thái pending
    transaction_id = add_transaction(user_id, 'deposit', amount, 'pending', description=None)
    context.user_data['last_deposit_transaction_id'] = transaction_id
    invoice_result = create_invoice(
        asset="USDT",
        amount=amount,
        description=get_text("deposit", lang) + f" - cybersillBot ({amount} USDT)",
        hidden_message=get_text("thank_you", lang) if get_text("thank_you", lang) else None
    )
    print("invoice_result: ", invoice_result)
    if invoice_result.get("ok"):
        invoice = invoice_result["result"]
        invoice_url = invoice["bot_invoice_url"]
        text = get_text("payment_instruction", lang).format(url=invoice_url)
        await update.message.reply_text(text, disable_web_page_preview=True)
    else:
        await update.message.reply_text(get_text("payment_error", lang))
    return ConversationHandler.END
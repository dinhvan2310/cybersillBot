import logging
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from telegram.constants import ParseMode

from db.repositories.user_repository import UserRepository
from db.repositories.product_repository import ProductRepository
from services.payment_service import PaymentService

logger = logging.getLogger(__name__)
payment_service = PaymentService()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /start command - introduce the bot and register the user"""
    user = update.effective_user
    
    # Register user in database
    await UserRepository.create_user(
        telegram_id=user.id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name
    )
    
    await update.message.reply_text(
        f"Hello, {user.first_name}! 👋\n\n"
        f"Your Telegram user ID is: {update.effective_user.id}\n\n"
        f"Welcome to CyberSill Bot. I can help you manage your balance and purchase software.\n\n"
        f"Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /help command - show available commands"""
    help_text = (
        "📋 *Available Commands*\n\n"
        "*User Commands*\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/balance - Check your current balance\n"
        "/addfunds - Add funds to your balance\n"
        "/profile - View your profile\n\n"
        
        "*Product Commands*\n"
        "/catalog - Browse available products\n"
        "/search <term> - Search for products\n"
        "/product <id> - View product details\n"
        "/buy <id> - Purchase a product\n\n"
        
        "*Admin Commands*\n"
        "/addproduct - Add a new product\n"
        "/editproduct <id> - Edit product\n"
        "/deleteproduct <id> - Delete product\n"
        "/stats - View statistics"
    )
    
    await update.message.reply_text(help_text, parse_mode=ParseMode.MARKDOWN)

async def balance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /balance command - show user's current balance"""
    user_id = update.effective_user.id
    balance = await payment_service.get_user_balance(user_id)
    
    await update.message.reply_text(
        f"💰 *Your Current Balance*\n\n"
        f"${balance:.2f}\n\n"
        f"To add funds, use /addfunds command.",
        parse_mode=ParseMode.MARKDOWN
    )

async def addfunds_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /addfunds command - initiate adding funds to balance"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text(
            "Please specify the amount to deposit.\n\n"
            "Example: /addfunds 10"
        )
        return
    
    try:
        amount = float(context.args[0])
        if amount <= 0:
            raise ValueError("Amount must be positive")
    except ValueError:
        await update.message.reply_text("Please enter a valid positive number.")
        return
    
    # Create deposit invoice
    result = await payment_service.create_deposit_invoice(user_id, amount)
    
    if not result.get("ok", False):
        await update.message.reply_text(
            f"❌ Error creating invoice: {result.get('error', 'Unknown error')}"
        )
        return
    
    invoice = result.get("result", {})
    pay_url = invoice.get("bot_invoice_url")
    
    await update.message.reply_text(
        f"💵 *Add Funds*\n\n"
        f"Amount: ${amount:.2f}\n"
        f"[Click here to pay]({pay_url})\n\n"
        f"Your balance will be updated automatically after payment.",
        parse_mode=ParseMode.MARKDOWN
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /profile command - show user's profile"""
    user_id = update.effective_user.id
    user = await UserRepository.get_user_by_telegram_id(user_id)
    
    if not user:
        await update.message.reply_text("Error retrieving your profile. Please try again.")
        return
    
    profile_text = (
        f"👤 *Your Profile*\n\n"
        f"User ID: {user['telegram_id']}\n"
        f"Username: {user['username'] or 'Not set'}\n"
        f"Name: {user['first_name']} {user['last_name'] or ''}\n"
        f"Balance: ${user['balance']:.2f}\n"
        f"Joined: {user['created_at'][:10]}"
    )
    
    await update.message.reply_text(profile_text, parse_mode=ParseMode.MARKDOWN)

async def catalog_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /catalog command - show all available products"""
    products = await ProductRepository.get_all_products()
    
    if not products:
        await update.message.reply_text("No products are available at the moment.")
        return
    
    catalog_text = "📚 *Product Catalog*\n\n"
    
    for product in products:
        catalog_text += (
            f"*{product.name}*\n"
            f"Price: ${product.price:.2f}\n"
            f"ID: {product.id}\n\n"
        )
    
    catalog_text += "To view product details, use /product <id>"
    
    await update.message.reply_text(catalog_text, parse_mode=ParseMode.MARKDOWN)

async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /search command - search for products"""
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("Please specify a search term.\n\nExample: /search python")
        return
    
    search_term = " ".join(context.args)
    products = await ProductRepository.search_products(search_term)
    
    if not products:
        await update.message.reply_text(f"No products found matching '{search_term}'.")
        return
    
    search_text = f"🔍 *Search Results for '{search_term}'*\n\n"
    
    for product in products:
        search_text += (
            f"*{product.name}*\n"
            f"Price: ${product.price:.2f}\n"
            f"ID: {product.id}\n\n"
        )
    
    search_text += "To view product details, use /product <id>"
    
    await update.message.reply_text(search_text, parse_mode=ParseMode.MARKDOWN)

async def product_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /product command - show product details"""
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("Please specify a product ID.\n\nExample: /product 1")
        return
    
    try:
        product_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid product ID.")
        return
    
    product = await ProductRepository.get_product_by_id(product_id)
    
    if not product:
        await update.message.reply_text(f"Product with ID {product_id} not found.")
        return
    
    product_text = (
        f"🛍️ *{product.name}*\n\n"
        f"{product.description}\n\n"
        f"Price: ${product.price:.2f}\n"
        f"ID: {product.id}\n\n"
        f"To purchase this product, use /buy {product.id}"
    )
    
    await update.message.reply_text(product_text, parse_mode=ParseMode.MARKDOWN)

async def buy_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle the /buy command - purchase a product"""
    user_id = update.effective_user.id
    
    if not context.args or len(context.args) < 1:
        await update.message.reply_text("Please specify a product ID.\n\nExample: /buy 1")
        return
    
    try:
        product_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Please enter a valid product ID.")
        return
    
    # Get product details
    product = await ProductRepository.get_product_by_id(product_id)
    
    if not product:
        await update.message.reply_text(f"Product with ID {product_id} not found.")
        return
    
    # Check user's balance
    balance = await payment_service.get_user_balance(user_id)
    
    if balance < product.price:
        await update.message.reply_text(
            f"❌ Insufficient balance.\n\n"
            f"Product Price: ${product.price:.2f}\n"
            f"Your Balance: ${balance:.2f}\n\n"
            f"Please add funds using /addfunds command."
        )
        return
    
    # Process purchase
    success = await payment_service.deduct_balance(user_id, product.price)
    
    if not success:
        await update.message.reply_text("❌ Error processing purchase. Please try again.")
        return
    
    # TODO: Store purchase record in database
    # TODO: Deliver the product (send file, etc.)
    
    await update.message.reply_text(
        f"✅ *Purchase Successful!*\n\n"
        f"You have purchased: *{product.name}*\n"
        f"Price: ${product.price:.2f}\n\n"
        f"Your file will be sent shortly.",
        parse_mode=ParseMode.MARKDOWN
    )

def register_command_handlers(application):
    """Register all command handlers"""
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("balance", balance_command))
    application.add_handler(CommandHandler("addfunds", addfunds_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(CommandHandler("catalog", catalog_command))
    application.add_handler(CommandHandler("search", search_command))
    application.add_handler(CommandHandler("product", product_command))
    application.add_handler(CommandHandler("buy", buy_command)) 
import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not configured")

if not ADMIN_ID:
    raise RuntimeError("ADMIN_ID is not configured")

ADMIN_ID = int(ADMIN_ID)

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    keyboard = [
        [
            InlineKeyboardButton("📝 Start Test", callback_data="start_test"),
            InlineKeyboardButton("🏆 Rank", callback_data="rank"),
        ],
        [
            InlineKeyboardButton("📊 My Result", callback_data="result"),
            InlineKeyboardButton("💎 Premium", callback_data="premium"),
        ],
        [
            InlineKeyboardButton("ℹ️ Help", callback_data="help"),
        ],
    ]

    await update.message.reply_text(
        f"👑 Welcome {user.first_name}!\n\n"
        "📚 *AdhikariBabu Test Bot*\n\n"
        "📝 MCQ Test\n"
        "🏆 Ranking\n"
        "📊 Result\n"
        "⏰ Scheduled Tests\n\n"
        "नीचे से option चुनें 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 Your Telegram User ID:\n\n`{update.effective_user.id}`",
        parse_mode="Markdown",
    )


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized access.")
        return

    await update.message.reply_text(
        "👑 *Admin Panel*\n\n"
        "📝 Add Questions\n"
        "📦 Bulk Questions\n"
        "📚 Create Test\n"
        "⏰ Schedule Test\n"
        "👥 Users\n"
        "🏆 Rankings\n"
        "📊 Statistics",
        parse_mode="Markdown",
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    messages = {
        "start_test": "📝 Test system जल्द तैयार होगा।",
        "rank": "🏆 अभी कोई test result उपलब्ध नहीं है।",
        "result": "📊 अभी कोई attempt उपलब्ध नहीं है।",
        "premium": "💎 Premium system जल्द जोड़ा जाएगा।",
        "help": "ℹ️ Help\n\n/start - Main Menu\n/myid - User ID\n/admin - Admin Panel",
    }

    await query.message.reply_text(
        messages.get(query.data, "Unknown option.")
    )


telegram_app.add_handler(CommandHandler("start", start))
telegram_app.add_handler(CommandHandler("myid", myid))
telegram_app.add_handler(CommandHandler("admin", admin))
telegram_app.add_handler(CallbackQueryHandler(button_handler))


@app.get("/")
def home():
    return "AdhikariBabu Test Bot is running."


@app.post("/webhook")
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)

    await telegram_app.initialize()
    await telegram_app.process_update(update)

    return "OK"


if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    app.run(host="0.0.0.0", port=port)

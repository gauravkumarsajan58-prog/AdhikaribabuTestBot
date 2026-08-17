import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# ---------- START ----------
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
        "नीचे से अपना option चुनें 👇",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


# ---------- MY ID ----------
async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🆔 आपका Telegram User ID:\n\n`{update.effective_user.id}`",
        parse_mode="Markdown",
    )


# ---------- BUTTONS ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "start_test":
        await query.message.reply_text(
            "📝 अभी Test System तैयार किया जा रहा है।\n\n"
            "जल्द ही यहाँ आपके सभी Tests दिखाई देंगे।"
        )

    elif query.data == "rank":
        await query.message.reply_text(
            "🏆 Leaderboard\n\n"
            "अभी कोई test attempt उपलब्ध नहीं है।"
        )

    elif query.data == "result":
        await query.message.reply_text(
            "📊 My Result\n\n"
            "आपने अभी कोई test attempt नहीं किया है।"
        )

    elif query.data == "premium":
        await query.message.reply_text(
            "💎 Premium Section\n\n"
            "Premium system जल्द जोड़ा जाएगा।"
        )

    elif query.data == "help":
        await query.message.reply_text(
            "ℹ️ Help\n\n"
            "📝 Test देकर अपना score प्राप्त करें।\n"
            "🏆 Leaderboard में rank देखें।\n"
            "📊 अपने results देखें।"
        )


# ---------- COMMANDS ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ AdhikariBabu Test Bot\n\n"
        "/start - Bot शुरू करें\n"
        "/myid - अपना Telegram ID देखें\n"
        "/help - Help"
    )


# ---------- MAIN ----------
def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable नहीं मिला।")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("myid", myid))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 AdhikariBabu Test Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()

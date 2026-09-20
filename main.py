import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

LINKS = {
    "ABC123": {
        "photo": "https://example.com/photo.jpg",
        "link": "https://example.com/cloud-file"
    },
    "XYZ789": {
        "photo": "https://example.com/photo2.jpg",
        "link": "https://example.com/cloud-file2"
    }
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send your code to get the file link."
    )


async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    code = update.message.text.strip().upper()

    if code not in LINKS:
        await update.message.reply_text(
            "Invalid code. Please check your code and try again."
        )
        return

    item = LINKS[code]

    keyboard = [
        [InlineKeyboardButton("Open File", url=item["link"])]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if item.get("photo"):
        await update.message.reply_photo(
            photo=item["photo"],
            reply_markup=reply_markup
        )
    else:
        await update.message.reply_text(
            "Here is your file link:",
            reply_markup=reply_markup
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code)
    )

    app.run_polling()


if __name__ == "__main__":
    main()

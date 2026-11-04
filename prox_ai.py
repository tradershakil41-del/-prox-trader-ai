import os
import asyncio
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    ContextTypes,
    filters
)
from google import genai

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_KEY)

async def reply_ai(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text

    prompt = f"""
You are PROX TRADER AI Assistant.
PROX TRADER is currently offline.
Reply helpfully and briefly in the user's language.
Never promise trading profits or guaranteed signals.
User message: {message}
"""

    try:
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=prompt
        )
        await update.message.reply_text(response.text)
    except Exception:
        await update.message.reply_text(
            "Sorry, AI is temporarily unavailable. Please try again."
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, reply_ai)
    )
    print("PROX TRADER AI is running!")
    app.run_polling()

if __name__ == "__main__":
    main()

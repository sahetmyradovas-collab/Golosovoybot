from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os

TOKEN = os.getenv("BOT_TOKEN")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.audio.file_id)
    path = "voice.ogg"
    await file.download_to_drive(path)

    # Указываем продолжительность вручную (например, 42 секунды)
    duration = 42

    with open(path, 'rb') as f:
        await update.message.reply_voice(voice=f, duration=duration)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.AUDIO | filters.Document.AUDIO, handle_audio))
    app.run_polling()

if __name__ == "__main__":
    main()

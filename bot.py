import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document.file_id)
    await file.download_to_drive("voice.ogg")

    await update.message.reply_text("🎵 Получено аудио, отправляю как голосовое...")

    with open("voice.ogg", "rb") as voice_file:
        await update.message.reply_voice(
            voice=voice_file,
            duration=42,  # длительность в секундах
            caption=None  # можно убрать
        )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.AUDIO | filters.Document.OGG, handle_audio))
    app.run_polling()

if __name__ == "__main__":
    main()

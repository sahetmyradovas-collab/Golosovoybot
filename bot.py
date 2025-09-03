import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем файл
    file = await context.bot.get_file(update.message.audio.file_id)
    await update.message.reply_text("🎵 Получено аудио, отправляю как голосовое...")
    # Скачиваем
    path = "audio.ogg"
    await file.download_to_drive(path)
    # Отправляем как voice
    with open(path, 'rb') as f:
        await update.message.reply_voice(voice=f)

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document.file_id)
    await update.message.reply_text("📁 Получен файл, пробую отправить как голосовое...")
    path = "audio.ogg"
    await file.download_to_drive(path)
    with open(path, 'rb') as f:
        await update.message.reply_voice(voice=f)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio))         # для .mp3
    app.add_handler(MessageHandler(filters.Document.AUDIO, handle_document))  # для отправки как файл
    app.run_polling()

if __name__ == "__main__":
    main()

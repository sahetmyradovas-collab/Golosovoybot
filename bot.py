import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Бот работает!")

# Новый обработчик голосовых сообщений
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_id = update.message.voice.file_id
    file = await context.bot.get_file(file_id)
    await update.message.reply_text("🎤 Голосовое получено. Сейчас скачаю файл...")
    # Сохраняем файл
    await file.download_to_drive(f"{file_id}.ogg")
    await update.message.reply_text("✅ Файл сохранён.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Обработчик голосов
    app.run_polling()

if __name__ == "__main__":
    main()

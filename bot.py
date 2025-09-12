import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

TOKEN = "8332887578:AAHSLW3m-JAO3v3F7LJBWSc75-lMHnFJbt0"

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.audio or update.message.voice or update.message.video or update.message.document
    if not file:
        return

    file_path = await file.get_file()
    await file_path.download_to_drive("input.mp3")

    # Конвертация в .ogg (voice с волнами)
    subprocess.run([
        "ffmpeg", "-i", "input.mp3",
        "-c:a", "libopus", "-b:a", "64k",
        "-ar", "48000", "-ac", "1",
        "voice.ogg"
    ])

    with open("voice.ogg", "rb") as f:
        await update.message.reply_voice(f)

    os.remove("input.mp3")
    os.remove("voice.ogg")

app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.AUDIO | filters.VOICE | filters.VIDEO | filters.Document.ALL, handle_audio))

print("✅ Бот запущен...")
app.run_polling()

import os
import speech_recognition as sr
from pydub import AudioSegment
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎙 Отправь мне голосовое сообщение, и я переведу его в текст!")

async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.voice.get_file()
    file_path = "voice.ogg"
    await file.download_to_drive(file_path)

    # Конвертация ogg → wav
    sound = AudioSegment.from_file(file_path, format="ogg")
    wav_path = "voice.wav"
    sound.export(wav_path, format="wav")

    # Распознавание речи
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        await update.message.reply_text(f"📝 Текст: {text}")
    except Exception as e:
        await update.message.reply_text("⚠️ Не удалось распознать речь.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VOICE, voice_handler))
    app.run_polling()

if __name__ == "__main__":
    main()

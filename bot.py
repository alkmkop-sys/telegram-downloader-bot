import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp
import aiohttp

BOT_TOKEN = os.getenv("8514940220:AAG8ZfuANiONTZBcNISVrvjTWTDX5w0gPgg")
CHANNEL_USERNAME = os.getenv("@english_quotes_ar")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id
    try:
        member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)
        if member.status not in ("member", "administrator", "creator"):
            await update.message.reply_text(f"👋 اشترك أولاً في القناة {CHANNEL_USERNAME} ثم أرسل الرابط.")
            return
    except:
        await update.message.reply_text(f"اشترك أولاً في القناة {CHANNEL_USERNAME} ثم أرسل الرابط.")
        return
    await update.message.reply_text("أرسل رابط الفيديو من يوتيوب أو تيك توك أو إنستغرام 🎥")

async def download_video(url: str):
    ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "youtube.com" in text or "youtu.be" in text or "tiktok.com" in text or "instagram.com" in text:
        await update.message.reply_text("⏳ جاري التحميل، انتظر قليلاً...")
        try:
            path = await download_video(text)
            await update.message.reply_video(video=open(path, "rb"))
        except Exception as e:
            await update.message.reply_text(f"❌ خطأ أثناء التحميل: {e}")
    else:
        await update.message.reply_text("أرسل رابطًا صحيحًا من يوتيوب أو تيك توك أو إنستغرام 🔗")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Bot started successfully!")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())

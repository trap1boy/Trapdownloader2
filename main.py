from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import re

from config import BOT_TOKEN, FORCE_CHANNEL, ADMIN_ID
from keep_alive import keep_alive
from downloader import youtube, instagram, tiktok, pinterest

bot = Client("TrapDownloaderBot", bot_token=BOT_TOKEN)

def check_membership(user_id):
    try:
        member = bot.get_chat_member(FORCE_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def get_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram.com" in url:
        return "instagram"
    elif "tiktok.com" in url:
        return "tiktok"
    elif "pinterest.com" in url:
        return "pinterest"
    else:
        return "unknown"

def join_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال", url=f"https://t.me/{FORCE_CHANNEL.strip('@')}")],
        [InlineKeyboardButton("✅ عضویت زدم، بررسی کن", callback_data="refresh")]
    ])

@bot.on_message(filters.command("start"))
def start(client, message: Message):
    if not check_membership(message.from_user.id):
        message.reply("🔒 برای استفاده از ربات باید عضو کانال بشی:", reply_markup=join_button())
        return
    message.reply("🎬 لینک ویدیوی YouTube، Instagram، TikTok یا Pinterest رو بفرست تا برات دانلود کنم.")

@bot.on_message(filters.private & filters.text)
def downloader(client, message: Message):
    if not check_membership(message.from_user.id):
        message.reply("🔒 برای استفاده از ربات باید عضو کانال بشی:", reply_markup=join_button())
        return

    url_match = re.search(r'https?://[^\s]+', message.text)
    if not url_match:
        message.reply("❌ لطفا یک لینک معتبر ارسال کن.")
        return

    url = url_match.group()
    platform = get_platform(url)
    message.reply("⏳ در حال پردازش لینک...")

    try:
        if platform == "youtube":
            result = youtube.download_youtube(url)
        elif platform == "instagram":
            result = instagram.download_instagram(url)
        elif platform == "tiktok":
            result = tiktok.download_tiktok(url)
        elif platform == "pinterest":
            result = pinterest.download_pinterest(url)
        else:
            message.reply("❌ این پلتفرم پشتیبانی نمی‌شود.")
            return

        if "error" in result:
            message.reply(f"❌ خطا: {result['error']}")
        else:
            message.reply(f"✅ عنوان: {result.get('title', 'بدون عنوان')}\n📥 لینک دانلود:\n{result.get('url')}")
    except Exception as e:
        message.reply(f"⚠️ خطا: {str(e)}")

@bot.on_callback_query(filters.regex("refresh"))
def refresh_join(client, callback_query):
    if check_membership(callback_query.from_user.id):
        callback_query.message.edit_text("✅ عضویت تأیید شد. حالا لینک بفرست.")
    else:
        callback_query.answer("❌ هنوز عضو نشدی!", show_alert=True)

keep_alive()
bot.run()

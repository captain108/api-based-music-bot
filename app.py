import asyncio
import requests
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import UserNotParticipant, ChatAdminRequired
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, Update
from pytgcalls.types.stream import StreamEnded
from config import *
from music_queue import add_song, next_song, get_queue

# ================= CLIENTS ================= #

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(user)

# ================= AUTO ASSISTANT ADD ================= #

async def ensure_assistant(chat_id):
    try:
        await user.get_chat_member(chat_id, "me")
        return True

    except UserNotParticipant:
        try:
            invite_link = await bot.export_chat_invite_link(chat_id)
            await user.join_chat(invite_link)
            return True
        except ChatAdminRequired:
            return False
        except Exception:
            return False

    except Exception:
        return False

# ================= FETCH API ================= #

async def fetch_api(query):
    r = requests.get(
        YTDLP_API,
        params={"key": YTDLP_KEY, "url": f"ytsearch:{query}"}
    )
    return r.json()

# ================= START ================= #

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=f"""
🎧 **{BOT_NAME}**

━━━━━━━━━━━━━━━━━━
🎵 Premium VC Music Bot  
👑 Owner: @{OWNER_USERNAME}
━━━━━━━━━━━━━━━━━━

Available Commands:

• /play
• /queue
• /ping
""",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🎵 Play", callback_data="help_play"),
                InlineKeyboardButton("📜 Queue", callback_data="help_queue")
            ],
            [
                InlineKeyboardButton("⚡ Ping", callback_data="help_ping")
            ],
            [
                InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}"),
                InlineKeyboardButton("💬 Support", url=f"https://t.me/{SUPPORT_GROUP}")
            ]
        ])
    )

# ================= PING ================= #

@bot.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply_photo(
        photo=PING_IMG_URL,
        caption="🏓 Pong!\nBot is Alive & Running 🚀"
    )

# ================= PLAY ================= #

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):

    if len(message.command) < 2:
        return await message.reply("Usage: /play song name")

    query = " ".join(message.command[1:])
    data = await fetch_api(query)

    if not data or not data.get("audio_url"):
        return await message.reply("❌ Failed to fetch audio.")

    song = {
        "title": data.get("title", "Unknown"),
        "audio_url": data["audio_url"],
        "thumbnail": data.get("thumbnail", STREAM_IMG_URL)
    }

    add_song(message.chat.id, song)

    # Ensure assistant in group
    assistant_ready = await ensure_assistant(message.chat.id)

    if not assistant_ready:
        return await message.reply_photo(
            photo=STREAM_IMG_URL,
            caption="""
❌ Assistant cannot join the group.

Possible Reasons:
• Assistant is banned
• Bot is not admin
• Invite permission disabled
"""
        )

    # Start playing if first in queue
    if len(get_queue(message.chat.id)) == 1:
        await call.join_group_call(
            message.chat.id,
            MediaStream(song["audio_url"])
        )

    await message.reply_photo(
        photo=song["thumbnail"],
        caption=f"""
🎶 **Started Streaming**

🎵 Title: {song['title']}
👤 Requested By: {message.from_user.mention}

━━━━━━━━━━━━━━━━━━
""",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("📜 Queue", callback_data="show_queue")
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ])
    )

# ================= QUEUE ================= #

@bot.on_message(filters.command("queue") & filters.group)
async def queue_cmd(_, message):
    queue = get_queue(message.chat.id)

    if not queue:
        return await message.reply_photo(
            photo=QUEUE_IMG_URL,
            caption="📭 Queue is empty."
        )

    text = "📜 **Current Queue:**\n\n"

    for i, song in enumerate(queue, start=1):
        text += f"{i}. {song['title']}\n"

    await message.reply_photo(
        photo=QUEUE_IMG_URL,
        caption=text
    )

# ================= CALLBACKS ================= #

@bot.on_callback_query()
async def callbacks(_, query):

    if query.data == "close":
        await query.message.delete()

    elif query.data == "show_queue":
        queue = get_queue(query.message.chat.id)
        text = "📜 **Current Queue:**\n\n"

        for i, song in enumerate(queue, start=1):
            text += f"{i}. {song['title']}\n"

        await query.message.edit_caption(text)

    elif query.data == "skip":
        next_track = next_song(query.message.chat.id)
        if next_track:
            await call.join_group_call(
                query.message.chat.id,
                MediaStream(next_track["audio_url"])
            )
            await query.answer("Skipped ⏭")
        else:
            await query.answer("No more songs in queue")

# ================= AUTO NEXT ================= #

@call.on_update()
async def stream_end_handler(_, update: Update):
    if isinstance(update, StreamEnded):
        chat_id = update.chat_id
        next_track = next_song(chat_id)

        if next_track:
            await call.join_group_call(
                chat_id,
                MediaStream(next_track["audio_url"])
            )

# ================= MAIN ================= #

async def main():
    await bot.start()
    await user.start()
    await call.start()
    print("Bot Running...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())

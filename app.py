import os
import random
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, Update
from pytgcalls.types.stream import StreamEnded
from config import *
from music_queue import add_song, next_song, get_queue

# Clients
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(user)

START_IMAGE_FOLDER = "assets"


# Random banner
def random_banner():
    files = os.listdir(START_IMAGE_FOLDER)
    images = [f for f in files if f.endswith((".jpg", ".png"))]
    return os.path.join(START_IMAGE_FOLDER, random.choice(images))


# Fetch API (supports song name)
async def fetch_api(query):
    r = requests.get(
        YTDLP_API,
        params={"key": YTDLP_KEY, "url": f"ytsearch:{query}"}
    )
    return r.json()


# Start command
@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_photo(
        photo=random_banner(),
        caption=f"""
🎧 **{BOT_NAME}**

Premium VC Music Bot
Owner: @{OWNER_USERNAME}
""",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("👑 Owner", url=f"https://t.me/{OWNER_USERNAME}")]
        ])
    )


# Play command
@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):

    if len(message.command) < 2:
        return await message.reply("Usage: /play song name")

    query = " ".join(message.command[1:])
    data = await fetch_api(query)

    if not data.get("audio_url"):
        return await message.reply("Failed to fetch audio.")

    song = {
        "title": data.get("title", "Unknown"),
        "audio_url": data["audio_url"],
        "thumbnail": data.get("thumbnail")
    }

    add_song(message.chat.id, song)

    # If first in queue, start playing
    if len(get_queue(message.chat.id)) == 1:
        await call.join_group_call(
            message.chat.id,
            MediaStream(song["audio_url"])
        )

    await message.reply_photo(
        photo=song["thumbnail"],
        caption=f"🎵 Added to queue:\n{song['title']}"
    )


# Auto Next (Modern v3 way)
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


# Main
async def main():
    await bot.start()
    await user.start()
    await call.start()
    print("Bot Running...")
    await asyncio.Event().wait()


asyncio.run(main())

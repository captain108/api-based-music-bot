import os
import random
import asyncio
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from config import *
from music_queue import add_song, next_song, get_queue
from player import play

# Clients
bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
user = Client("user", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
call = PyTgCalls(user)

START_IMAGE_FOLDER = "assets"

def random_banner():
    files = os.listdir(START_IMAGE_FOLDER)
    images = [f for f in files if f.endswith((".jpg", ".png"))]
    return os.path.join(START_IMAGE_FOLDER, random.choice(images))

async def fetch_api(url):
    r = requests.get(f"{YTDLP_API}?key={YTDLP_KEY}&url={url}")
    return r.json()

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

@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, message):

    if len(message.command) < 2:
        return await message.reply("Usage: /play youtube_link")

    data = await fetch_api(message.command[1])

    if not data.get("audio_url"):
        return await message.reply("Failed to fetch audio.")

    song = {
        "title": data["title"],
        "audio_url": data["audio_url"],
        "thumbnail": data["thumbnail"]
    }

    add_song(message.chat.id, song)

    if len(get_queue(message.chat.id)) == 1:
        await play(call, message.chat.id, song)

    await message.reply_photo(
        photo=song["thumbnail"],
        caption=f"🎵 Added to queue:\n{song['title']}"
    )

@call.on_stream_end()
async def stream_end(_, update):
    next_track = next_song(update.chat_id)
    if next_track:
        await play(call, update.chat_id, next_track)

async def main():
    await bot.start()
    await user.start()
    await call.start()
    print("Bot Running...")
    await asyncio.Event().wait()

asyncio.get_event_loop().run_until_complete(main())

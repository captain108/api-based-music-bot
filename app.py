from queue import add_to_queue, get_next
from player import play_song

@bot.on_message(filters.command("play") & filters.group)
async def play(_, message):

    url = message.command[1]
    data = await get_stream_data(url)

    song = {
        "title": data["title"],
        "audio_url": data["audio_url"],
        "thumbnail": data["thumbnail"]
    }

    add_to_queue(message.chat.id, song)

    if len(get_queue(message.chat.id)) == 1:
        await play_song(call, message.chat.id, song)

    await message.reply(f"🎵 Added to queue: {song['title']}")

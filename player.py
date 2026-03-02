import asyncio
from queue import get_next
from pytgcalls.types.input_stream import InputStream, AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

async def play_song(call, chat_id, song):
    await call.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(song["audio_url"], HighQualityAudio())
        )
    )

async def auto_next(call, chat_id):
    while True:
        await asyncio.sleep(1)
        next_song = get_next(chat_id)
        if next_song:
            await play_song(call, chat_id, next_song)

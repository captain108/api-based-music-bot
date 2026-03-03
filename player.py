from pytgcalls.types import MediaStream

async def play(call, chat_id, song):
    await call.join_group_call(
        chat_id,
        MediaStream(song["audio_url"])
    )

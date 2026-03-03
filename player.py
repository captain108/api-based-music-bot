from pytgcalls.types.input_stream import AudioPiped

async def play(call, chat_id, song):
    await call.join_group_call(
        chat_id,
        AudioPiped(song["audio_url"])
    )

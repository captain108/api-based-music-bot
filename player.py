from pytgcalls.types.input_stream import InputStream, AudioPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio

async def play(call, chat_id, song):
    await call.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(
                song["audio_url"],
                HighQualityAudio()
            )
        )
    )

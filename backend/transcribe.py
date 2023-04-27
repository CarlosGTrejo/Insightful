import asyncio

import audio_utils
import utils
import whisper
from deepgram import Deepgram


# Get api key
with open('deepgram_key', 'r') as f:
    key = f.read().strip()

options = {
    'language': 'en',
    'task': 'transcribe'
}

model = whisper.load_model('base.en', device='cuda', download_root='./models')


def using_whisper(audio_bytes: bytes) -> str:
    audio = audio_utils.load_audio(audio_bytes)
    result = model.transcribe(audio, **options)
    transcript = result.get('text')
    if not isinstance(transcript, str):
        transcript = 'No transcript available'
    return transcript


async def using_deepgram(audio: bytes, mimetype: str):
    deepgram = Deepgram(key)

    source = {
        'buffer': audio,
        'mimetype': mimetype
    }
    options = {
        'punctuate': True,
        'summarize': True,
        'numerals': True,
        'model': 'nova',
        'language': 'en'
    }

    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            options
        )
    )

    summary = utils.get_summary(response)
    transcript = utils.get_transcript(response)

    return transcript, summary

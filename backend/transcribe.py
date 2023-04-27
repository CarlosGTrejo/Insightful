import asyncio

import audio_utils
import utils
import whisper
from deepgram import Deepgram


# Get deepgram api key
with open('deepgram_key', 'r') as f:
    key = f.read().strip()


def using_whisper(audio_bytes: bytes) -> str:
    model = whisper.load_model('base.en', device='cuda', download_root='./models')
    options = {
        'language': 'en',
        'task': 'transcribe'
    }
    audio = audio_utils.load_audio(audio_bytes)
    result = model.transcribe(audio, **options)
    transcript = result.get('text')
    if not isinstance(transcript, str):
        transcript = 'No transcript available'
    return transcript


async def using_deepgram(audio: bytes, mimetype: str) -> tuple[tuple[tuple[str, float]], str]:
    '''Transcribes audio with deepgram and returns a tuple of the words and summary
    tuple(tuple(word, timestamp), summary)
    words: tuple[tuple[str, float]] = Holds the words of the transcript and their timestamp
    summary: str'''
    deepgram = Deepgram(key)

    source = {
        'buffer': audio,
        'mimetype': mimetype
    }
    options = {
        'punctuate': True,  # Capitalize, add periods, commas, etc.
        'summarize': True,  # Generate a summary for sections of the transcript
        'numerals': True,  # Change word numbers to digit numbers (eg. one -> 1)
        'model': 'nova',  # Deepgram's latest ARS at the time of writing this
        'language': 'en'
    }

    response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            options
        )
    )

    summary = utils.get_summary(response)
    # transcript = utils.get_transcript(response)
    words = utils.get_words(response)

    return words, summary

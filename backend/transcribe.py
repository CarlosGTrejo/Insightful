import whisper
import audio_utils

options = {
    'language': 'en',
    'task': 'transcribe'
}

model = whisper.load_model('base', device='cuda', download_root='./models')


def transcription_pipeline(audio_bytes: bytes) -> str:
    audio = audio_utils.load_audio(audio_bytes)
    result = model.transcribe(audio, **options)
    transcript = result.get('text')
    if not isinstance(transcript, str):
        transcript = 'No transcript available'
    return transcript

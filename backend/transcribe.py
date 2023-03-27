import whisper

model = whisper.load_model('base')

options = {
    'language': 'en',
    'task': 'transcribe'
}

result = model.transcribe('back-to-the-future.mp3', word_timestamps=True, **options)


with open('back-to-the-future.mp3', 'rb') as f:
    file_bytes = f.read()

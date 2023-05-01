import json


def _get_main_content(response):
    '''Returns the first object in the "alternatives" field from a deepgram json response.'''
    return response['results']['channels'][0]['alternatives'][0]


def get_summaries(response) -> list[dict]:
    '''Returns the summaries portion of the json response
    summaries: [{summary: str, start_word: int, end_word: int}, ...]'''
    return _get_main_content(response)['summaries']


def get_transcript(response) -> str:
    transcript = _get_main_content(response)['transcript']
    return transcript


def get_words(response) -> tuple[tuple[str, float, float]]:
    '''Returns a tuple of tuples that has the values (punctuated_word, start, end).

    punctuated_word: str = The word of the transcript with proper punctuation
    start: float = The time in the audio clip that the beginning of the word is heard
    end: float = The time in the audio clip that the word ends.'''
    words = tuple(
        (d['punctuated_word'], round(d['start'], 2), round(d['end'], 2))
        for d
        in _get_main_content(response)['words']
    )
    return words


def dev() -> tuple[tuple[tuple[str, float, float]], list[dict]]:
    '''Returns sample data from a Back to the Future clip for testing purposes.'''
    with open('response-summarize-numerals.json', 'r') as f:
        response = json.load(f)

    transcript = get_words(response)
    summary = get_summaries(response)
    return transcript, summary


def words_to_transcript(word_array: tuple[tuple[str, float, float]]) -> str:
    return ' '.join([arr[0] for arr in word_array])

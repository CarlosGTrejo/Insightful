import json


def _get_main_content(response):
    '''Returns the first object in the "alternatives" field from a deepgram json response.'''
    return response['results']['channels'][0]['alternatives'][0]


def dev() -> tuple[tuple[tuple[str, float, float]], str]:
    '''Returns sample data from a Back to the Future clip for testing purposes.'''
    with open('response-summarize-numerals.json', 'r') as f:
        response = json.load(f)

    transcript = get_words(response)
    summary = '\n\n'.join([
        summary_dict['summary']
        for summary_dict
        in _get_main_content(response)['summaries']
    ])
    return transcript, summary


def get_summary(response) -> str:
    summary = '\n\n'.join([
        summary_dict['summary']
        for summary_dict
        in _get_main_content(response)['summaries']
    ])
    return summary


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

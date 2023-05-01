import openai

with open('openai_key', 'r') as f:
    openai.api_key = f.read().strip()


def summarize(text: str) -> str:
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user',
                'content': f'{text}\n\n' \
                'Write a summary of the prior text that highlights its key points. ' \
                'Use the least number of words as possible in your summary, ' \
                'only write what is essential.'
            }
        ]
    )
    response = completion.choices[0].message.content
    return response

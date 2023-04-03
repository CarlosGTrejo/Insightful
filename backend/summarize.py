from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

model_name = 'facebook/bart-large-cnn'
tokenizer = AutoTokenizer.from_pretrained(model_name, model_max_length=1024)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


def summarize_text(text):
    try:
        summary = model.generate(**tokenizer(text, return_tensors="pt"))[0]
        return tokenizer.decode(summary, skip_special_tokens=True)
    except IndexError:
        return summarize_text(text[:len(text) // 2]) + summarize_text(text[len(text) // 2:])


def summarize_v2(text, max_len: int):
    input_ids = tokenizer.encode(text, return_tensors='pt', max_length=512, truncation=True)
    summary_ids = model.generate(input_ids, max_length=max_len, min_length=32, length_penalty=2.0, num_beams=4, early_stopping=True, do_sample=False, repetition_penalty=1.0, no_repeat_ngram_size=3, diversity_penalty=0.0, )
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary


def summarize_v3(text, max_len: int = 256):
    summarizer = pipeline('summarization', model=model_name)
    try:
        summary = summarizer(text, max_length=max_len, min_length=24, do_sample=False)
        return summary[0]['summary_text']
    except IndexError:
        half = len(text // 2)
        return summarize_v3(text[:half], max_len=max_len // 2) + summarize_v3(text[half:], max_len=max_len // 2)


if __name__ == '__main__':

    input_text = "The United States is experiencing a surge in COVID-19 cases, with many states reporting record numbers of new infections. The rise in cases is believed to be due to the spread of the highly contagious Delta variant, as well as low vaccination rates in some parts of the country."

    print('v2')
    print(summarize_v2(input_text))
    print('\n\nv3')
    print(summarize_v3(input_text))

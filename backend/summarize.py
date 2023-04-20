from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import torch


device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
model_name = 'bigscience/bloomz-3b'
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype='auto', device_map='auto', offload_folder='offload', offload_state_dict=True).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)


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


def bloomz(text):
    inputs = tokenizer.encode('Summarize the following text: ' + text, return_tensors='pt').to(device)
    outputs = model.generate(inputs)
    return tokenizer.decode(outputs[0], skip_special_tokens=True, clean_up_tokenization_spaces=False)


if __name__ == '__main__':

    input_text = "The United States is experiencing a surge in COVID-19 cases, with many states reporting record numbers of new infections. The rise in cases is believed to be due to the spread of the highly contagious Delta variant, as well as low vaccination rates in some parts of the country."

    print(bloomz(input_text))

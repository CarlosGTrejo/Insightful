import torch
import csv
from transformers import PegasusForConditionalGeneration, PegasusTokenizer, Trainer, TrainingArguments


device = "cuda" if torch.cuda.is_available() else "cpu"
# Load the pre-trained PEGASUS-XSUM model and tokenizer
model = PegasusForConditionalGeneration.from_pretrained('google/pegasus-xsum').to(device)
tokenizer = PegasusTokenizer.from_pretrained('google/pegasus-xsum')

# Prepare your data


# Define a function to preprocess your data
def preprocess_function(examples):
    input_encodings = tokenizer(examples['text'], truncation=True, padding='max_length')
    prompt_encodings = tokenizer(examples['prompt'], truncation=True, padding='max_length')
    output_encodings = tokenizer(examples['summary'], truncation=True, padding='max_length')

    encodings = {
        'input_ids': input_encodings['input_ids'],
        'attention_mask': input_encodings['attention_mask'],
        'decoder_input_ids': prompt_encodings['input_ids'],
        'decoder_attention_mask': prompt_encodings['attention_mask'],
        'labels': output_encodings['input_ids'],
    }

    return encodings


# Preprocess your data
with open('C:/Repos/Insightful/backend/train.csv', 'r') as f:
    reader = csv.DictReader(f)
    train_data = list(reader)

train_dataset = torch.utils.data.Dataset(train_data)
train_dataset = train_dataset.map(preprocess_function, batched=True)

# Define your training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=10,
    per_device_train_batch_size=4,
    save_steps=500,
    save_total_limit=2,
    gradient_accumulation_steps=16,
)

# Define your trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

# Fine-tune your model
trainer.train()

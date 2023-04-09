from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Load the PEGASUS-X model
tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum", torch_dtype='auto', offload_folder='offload', offload_state_dict=True)

text = "In this lesson, we will learn about the different types of clouds that exist in the atmosphere. Clouds are classified based on their height, shape, and composition. The three main cloud types are cumulus, stratus, and cirrus. Cumulus clouds are puffy and white, with a flat base and a rounded top. Stratus clouds are low, gray, and flat, and they often cover the entire sky. Cirrus clouds are high and thin, with a wispy appearance. They are often an indicator of an approaching storm. Understanding the different cloud types is important for weather forecasting and aviation safety."

inputs = tokenizer.encode(text, return_tensors="pt")

# Generate the summary
outputs = model.generate(inputs, max_new_tokens=128)
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

print(summary)

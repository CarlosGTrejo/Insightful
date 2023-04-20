from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

model_name = 'bigscience/bloomz-3b'
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, torch_dtype='auto', device_map='auto', offload_folder='offload', offload_state_dict=True)

text = '''Now there are rules to Lewis structures, and here is the complete rule. In your handout, this wouldn't fit on one page. It's on two pages. And these rules, if you do work these problems, you will remember these rules, and they become pretty easy. But it's important to work Lewis structure problems so that the rules become really familiar to you. And it takes time to work Lewis structure problems, so don't wait to the last minute to start this problem set. There's a lot of Lewis structure problems on it, which means it's not difficult, but it's going to take some time. All right. So let's briefly go over these rules. First what you want to do is draw in the skeleton structure. Just put the atoms down. Hydrogen and fluorine are always going to be terminal atoms. Don't put them in the middle of a molecule. That gets chemistry professors really upset to see hydrogen in the middle with lots of bonds to things, so don't do it. And typically the element with the lowest ionization energy goes in the middle, and there are some exceptions and we'll see some of those exceptions. But that should be your first guess. You want to count the number of valence electrons. If there's a negative charge, you need to count that in or if there's a positive charge you need to subtract that from the total. Then you want to figure out the total number of electrons needed, so everyone has their full valence shell. You need to subtract these two to get the number of bonding electrons. And here are some of the things that it's really easy to make math mistakes here, so if your structure makes zero sense at the end, go back and check your math. Assign to bonding electrons to each bond. If any remain, you want to think about whether you have double or triple bonds. And there's only certain kinds of atoms that can have double and triple bonds. So be careful where you're putting your double and triple bonds. If any valence electrons remain, those are lone pairs. And then lastly, you want to figure out the formal charge on all of the atoms in your structure to make sure that this is a valid structure, and we're going to talk about formal charge. So first, let's just try an example.

Write a summary of the prior text that highlights its key points:

To draw Lewis structures, place the atoms in a skeleton structure, count the number of valence electrons while adding negative charges or subtracting if there are positive charges. Then calculate the electrons needed to fulfill the valance shell of each atom. Then, use bonding electrons to form bonds, remaining bonds may be due to a double or triple bond. Any remaining electrons after that are lone pairs. Lastly, calculate the formal charge of all the atoms to verify if the structure is valid. Hydrogen and fluorine are always terminal atoms and the element with the lowest ionization energy typically goes in the middle. Double and triple bonds are only allowed for certain atoms.


In this lesson, we will learn about the different types of clouds that exist in the atmosphere. Clouds are classified based on their height, shape, and composition. The three main cloud types are cumulus, stratus, and cirrus. Cumulus clouds are puffy and white, with a flat base and a rounded top. Stratus clouds are low, gray, and flat, and they often cover the entire sky. Cirrus clouds are high and thin, with a wispy appearance. They are often an indicator of an approaching storm. Understanding the different cloud types is important for weather forecasting and aviation safety.'''

inputs = tokenizer.encode(f'{text}\n\nWrite a summary of the prior text that highlights its key points.', return_tensors="pt").to(device)
outputs = model.generate(inputs, max_new_tokens=64)

summary = tokenizer.decode(outputs[0], skip_special_tokens=False)

print(summary)

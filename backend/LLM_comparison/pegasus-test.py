from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch


model_name = "google/pegasus-xsum"
device = "cuda" if torch.cuda.is_available() else "cpu"

text = [
    " PG&E Now there are rules to Lewis structures, and here is the complete rule. In your handout, this wouldn't fit on one page. It's on two pages. And these rules, if you do work these problems, you will remember these rules, and they become pretty easy. But it's important to work Lewis structure problems so that the rules become really familiar to you. And it takes time to work Lewis structure problems, so don't wait to the last minute to start this problem set. There's a lot of Lewis structure problems on it, which means it's not difficult, but it's going to take some time. All right. So let's briefly go over these rules. First what you want to do is draw in the skeleton structure. Just put the atoms down. Hydrogen and fluorine are always going to be terminal atoms. Don't put them in the middle of a molecule. That gets chemistry professors really upset to see hydrogen in the middle with lots of bonds to things, so don't do it. And typically the element with the lowest ionization energy goes in the middle, and there are some exceptions and we'll see some of those exceptions. But that should be your first guess. You want to count the number of valence electrons. If there's a negative charge, you need to count that in or if there's a positive charge you need to subtract that from the total. Then you want to figure out the total number of electrons needed, so everyone has their full valence shell. You need to subtract these two to get the number of bonding electrons. And here are some of the things that it's really easy to make math mistakes here, so if your structure makes zero sense at the end, go back and check your math. Assign to bonding electrons to each bond. If any remain, you want to think about whether you have double or triple bonds. And there's only certain kinds of atoms that can have double and triple bonds. So be careful where you're putting your double and triple bonds. If any valence electrons remain, those are lone pairs. And then lastly, you want to figure out the formal charge on all of the atoms in your structure to make sure that this is a valid structure, and we're going to talk about formal charge. So first, let's just try an example."
    ]


tokenizer = PegasusTokenizer.from_pretrained(model_name)
model = PegasusForConditionalGeneration.from_pretrained(model_name).to(device)
batch = tokenizer(text, truncation=True, padding="longest", return_tensors="pt").to(device)
translated = model.generate(max_new_tokens=128, **batch)
tgt_text = tokenizer.batch_decode(translated, skip_special_tokens=True)

print(tgt_text[0])

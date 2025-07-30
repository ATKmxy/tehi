# Initializer for Tehi Kernel

from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("TheUnlocked/tehi-v1")
tokenizer = AutoTokenizer.from_pretrained("TheUnlocked/tehi-v1")

inputs = tokenizer("מה את באמת?", return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=256)

print(tokenizer.decode(outputs[0]))

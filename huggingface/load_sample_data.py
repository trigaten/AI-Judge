from datasets import load_dataset
from transformers import AutoTokenizer

dataset = load_dataset('csv', data_files="sample_data.csv")
print(dataset)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

posts = [line["post"] for line in dataset["train"]]
comments = [line["comment"] for line in dataset["train"]]

model_inputs = tokenizer(posts, truncation=True, padding=True)
model_outputs = tokenizer(comments, truncation=True, padding=True)
print(model_inputs)
print(model_outputs)


tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token

posts = [line["post"] for line in dataset["train"]]
comments = [line["comment"] for line in dataset["train"]]

model_inputs = tokenizer(posts, truncation=True, padding=True)
model_outputs = tokenizer(comments, truncation=True, padding=True)

# print(tokenized_dataset["train"][0])

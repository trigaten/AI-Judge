from datasets import load_dataset
from transformers import AutoTokenizer
path = "sample_data.csv" 
dataset2 = load_dataset('csv', data_files=path,
                        split="train").train_test_split(test_size=0.2)
print(dataset2)

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token


def preprocess_function(examples):
    return tokenizer(examples["post"],
                     examples["comment"],
                     truncation=True,
                     padding=True)


tokenized_dataset2 = dataset2.map(preprocess_function, batched=True)
print(tokenized_dataset2)
print(tokenized_dataset2["train"][0])
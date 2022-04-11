from datasets import load_dataset
dataset = load_dataset('csv', data_files='sample_data.csv')

print(dataset)
print(dataset["train"][0])
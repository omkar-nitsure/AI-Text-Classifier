import datasets

dataset = datasets.load_dataset('openwebtext-10k.py', trust_remote_code=True)

with open("openwebtext_dataset.txt", "w", encoding="utf-8") as f:
    for sample in dataset['train']:
        f.write(sample['text'])

with open("openwebtext_dataset.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

text = []
text = lines[0][:-1]
for i in range(len(lines)):
    if(lines[i] == "\n"):
        continue
    else:
        text += lines[i][:-1]


with open("data_merged.txt", "w", encoding="utf-8") as f:
    f.write(text)
f.close()

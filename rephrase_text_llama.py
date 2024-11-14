import torch
import os
import json
from transformers import pipeline

model_id = "meta-llama/Llama-3.2-3B-Instruct"

pipe = pipeline("text-generation", model=model_id, torch_dtype=torch.bfloat16, device=7)

n_loads = 100

sys_prompt = {
    "role": "system",
    "content": "Perform sentence restructuring while keeping the paragraph length similar and make sure the rephrased text seems like written by AI. Don't include description of what you did",
}

os.makedirs("AI-big", exist_ok=True)


def load_shard(shard_path, start_idx, n_loads):
    with open(shard_path, "r") as f:
        data = json.load(f)
    f.close()
    end_idx = max(start_idx + n_loads, len(data))
    data_chunk = {k: data[k] for k in list(data.keys())[start_idx:end_idx]}
    del data
    return data_chunk


def count_chunks(shard_path, n_loads):
    with open(shard_path, "r") as f:
        data = json.load(f)
    f.close()
    return len(data) // n_loads + 1


shards = os.listdir("AI-Text-Classifier/fineweb_data/data")

dict = {}
for i in range(len(shards)):
    num = ""
    for j in range(len(shards[i])):
        if shards[i][j].isdigit():
            num += shards[i][j]

    dict[int(num)] = shards[i]

del shards
dict = dict.items()
dict = sorted(dict)
shards = []

for i in range(len(dict)):
    shards.append(dict[i][1])

del dict

for i in range(2, len(shards)):
    start_idx = 0
    shard_path = "AI-Text-Classifier/fineweb_data/data/" + shards[i]
    filename = "AI-big/" + shards[i]

    n_chunks = count_chunks(shard_path, n_loads)

    for i in range(n_chunks):
        data = load_shard(shard_path, start_idx, n_loads)
        keys = list(data.keys())

        for j in range(0, len(keys)):
            messages = [sys_prompt]
            messages.append({"role": "user", "content": data[keys[j]]})

            outputs = pipe(messages, max_new_tokens=1024)

            with open(filename, "a") as json_file:
                json_file.write(
                    json.dumps({keys[j]: outputs[0]["generated_text"][-1]}) + "\n"
                )
        start_idx += n_loads

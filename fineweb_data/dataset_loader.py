import pandas as pd
import os
import json

def parquet_to_json(parquet_file, text_column, output_folder, num_shards):
    os.makedirs('data', exist_ok=True)
    df = pd.read_parquet(parquet_file)
    if text_column not in df.columns:
        raise ValueError(f"Column '{text_column}' not found in the Parquet file.")
    
    output_files = output_folder + "/shard_"

    shard_size = len(df[text_column]) // num_shards

    for i in range(num_shards):

        if(i == num_shards - 1):
            texts = df[text_column].iloc[i*shard_size:]
        else:
            texts = df[text_column].iloc[i*shard_size:(i+1)*shard_size]

        final_texts = [text.replace('\n', ' ') for text in texts]

        json_file = output_files + f"{i}.json"
        json_data = {str(j + 1).zfill(6): text for j, text in enumerate(final_texts)}

        with open(json_file, 'w') as f:
            json.dump(json_data, f, indent=4)
        f.close()

        print(f"Shard {i} written to {json_file}")

    print(f"Text data sharded and written successfully!")

if __name__ == "__main__":
    parquet_file = 'train-00000-of-00030.parquet'  # Specify the Parquet file path
    text_column = 'text'  # Specify the name of the column that contains the text data
    output_folder = 'data'  # Specify the output folder path
    num_shards = 100  # Specify the number of shards to split the output file into

    parquet_to_json(parquet_file, text_column, output_folder, num_shards)

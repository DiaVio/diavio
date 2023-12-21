"""
This script includes functions for evaluating natural language generation models. It calculates various NLG metrics
such as BLEU, METEOR, and ROUGE_L. The script utilizes the NLGEval library to compute these metrics and supports both
evaluation and aggregation of results across multiple files.
"""

import os
import json
from tqdm import tqdm
from nlgeval import compute_metrics


def nlgeval_metrics(save_folder, reason_folder, dataset_folder):
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for filename in tqdm(os.listdir(reason_folder)):
        hypothesis = os.path.join(reason_folder, filename)
        references = [os.path.join(dataset_folder, filename)]
        try:
            metrics_dict = compute_metrics(hypothesis, references)
            # Save metrics in .json format
            filename = filename.replace('.txt', '.json')
            with open(os.path.join(save_folder, filename), 'w') as f:
                f.write(json.dumps(metrics_dict, indent=4))

        except AssertionError:
            print(f"Error with file: {filename}")
            continue

# Calculate the average values of Bleu_4, METEOR, and ROUGE_L for the target_model


def calnlgeval(target_model, target_folder):
    Bleu1 = []
    Bleu2 = []
    Bleu3 = []
    Bleu4 = []
    METEOR = []
    ROUGE_L = []
    for filename in tqdm(os.listdir(target_folder)):
        # Read each json file in the folder and calculate the average of each metric
        with open(os.path.join(target_folder, filename), 'r') as f:
            data = json.load(f)
            # Record the values of each metric in a list
            Bleu1.append(data['Bleu_1'])
            Bleu2.append(data['Bleu_2'])
            Bleu3.append(data['Bleu_3'])
            Bleu4.append(data['Bleu_4'])
            METEOR.append(data['METEOR'])
            ROUGE_L.append(data['ROUGE_L'])

    Bleu1_mean = sum(Bleu1) / len(Bleu1)
    Bleu2_mean = sum(Bleu2) / len(Bleu2)
    Bleu3_mean = sum(Bleu3) / len(Bleu3)
    Bleu4_mean = sum(Bleu4) / len(Bleu4)
    METEOR_mean = sum(METEOR) / len(METEOR)
    ROUGE_L_mean = sum(ROUGE_L) / len(ROUGE_L)

    print(f"========{target_model}========")
    print(f"Bleu1: {Bleu1_mean}")
    print(f"Bleu2: {Bleu2_mean}")
    print(f"Bleu3: {Bleu3_mean}")
    print(f"Bleu4: {Bleu4_mean}")
    print(f"METEOR: {METEOR_mean}")
    print(f"ROUGE_L: {ROUGE_L_mean}")

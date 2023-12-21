"""
This script contains functions to calculate various evaluation metrics for machine learning models.
These include accuracy, precision, recall, F1 score (macro and micro averaged), BERTScore, BLEURT and NUBIA score.
"""

import os
from tqdm import tqdm


def calAcc(model, label_folder, dataset_folder):
    # Record the TP, FP, FN values for each category using dictionaries
    TP = {}
    FP = {}
    FN = {}

    for filename in tqdm(os.listdir(dataset_folder)):
        with open(os.path.join(dataset_folder, filename), 'r') as datasetlabel_file:
            datasetlabel = datasetlabel_file.read()  # Actual label

        with open(os.path.join(label_folder, filename), 'r') as label_file:
            label = label_file.read()  # Predicted label

        # Ensure all labels are keys in the dictionaries
        TP.setdefault(datasetlabel, 0)
        FP.setdefault(datasetlabel, 0)
        FN.setdefault(datasetlabel, 0)
        TP.setdefault(label, 0)
        FP.setdefault(label, 0)
        FN.setdefault(label, 0)

        if datasetlabel == label:
            TP[datasetlabel] += 1
        else:
            FP[label] += 1
            FN[datasetlabel] += 1

    # Calculate Precision and Recall
    Precision = {}
    Recall = {}
    all_keys = set(TP.keys()).union(FP.keys(), FN.keys())
    for key in all_keys:
        Precision[key] = TP[key] / \
            (TP[key] + FP[key]) if TP[key] + FP[key] != 0 else 0
        Recall[key] = TP[key] / \
            (TP[key] + FN[key]) if TP[key] + FN[key] != 0 else 0

    # Output the results
    print(f"========{model}========")
    print(f"Accuracy: {sum(TP.values()) / len(os.listdir(dataset_folder))}")
    print(f"Precision: {Precision}")
    print(f"Recall: {Recall}")

    # Calculate Macro-average
    Macro_Precision = sum(Precision.values()) / len(Precision)
    Macro_Recall = sum(Recall.values()) / len(Recall)
    Macro_f1_score = 2 * Macro_Precision * Macro_Recall / \
        (Macro_Precision + Macro_Recall) if (Macro_Precision + Macro_Recall) != 0 else 0
    print('------Macro------')
    print(f"Macro_Precision: {Macro_Precision}")
    print(f"Macro_Recall: {Macro_Recall}")
    print(f"Macro_f1_score: {Macro_f1_score}")

    # Calculate Micro-average
    Micro_Precision = sum(TP.values()) / (sum(TP.values()) + sum(FP.values()))
    Micro_Recall = sum(TP.values()) / (sum(TP.values()) + sum(FN.values()))
    Micro_f1_score = 2 * Micro_Precision * Micro_Recall / \
        (Micro_Precision + Micro_Recall) if (Micro_Precision + Micro_Recall) != 0 else 0
    print('------Micro------')
    print(f"Micro_Precision: {Micro_Precision}")
    print(f"Micro_Recall: {Micro_Recall}")
    print(f"Micro_f1_score: {Micro_f1_score}")


def calBertScore(model, bert_score_folder):
    # Calculate the mean BERT score from the scores in a folder
    bert_score_mean = {}
    bert_score_P = 0
    bert_score_R = 0
    bert_score_F1 = 0
    filename_list = os.listdir(bert_score_folder)
    for filename in tqdm(filename_list):
        with open(os.path.join(bert_score_folder, filename), 'r') as bert_score_file:
            bert_score = bert_score_file.read()
            bert_score_P += eval(bert_score)["P"]
            bert_score_R += eval(bert_score)["R"]
            bert_score_F1 += eval(bert_score)["F1"]

    bert_score_mean["P"] = bert_score_P / len(filename_list)
    bert_score_mean["R"] = bert_score_R / len(filename_list)
    bert_score_mean["F1"] = bert_score_F1 / len(filename_list)
    print(f"========{model}========")
    print(f"bert_score_mean: {bert_score_mean}")


def calBleurt(model, bleurt_file):
    # Read each line of the BLEURT file and calculate the mean score
    with open(bleurt_file, 'r') as bleurt_file:
        bleurt_list = bleurt_file.readlines()
    for i in tqdm(range(len(bleurt_list))):
        bleurt_list[i] = float(bleurt_list[i].strip('\n'))
    bleurt_mean = sum(bleurt_list) / len(bleurt_list)

    print(f"========{model}========")
    print(f"bleurt_mean: {bleurt_mean}")


def calNubia(model, nubia_file):
    # Read each line of the NUBIA file and calculate the mean score
    with open(nubia_file, 'r') as nubia_file:
        nubia_list = nubia_file.readlines()
    for i in tqdm(range(len(nubia_list))):
        nubia_list[i] = float(nubia_list[i].strip('\n'))
    nubia_mean = sum(nubia_list) / len(nubia_list)

    print(f"========{model}========")
    print(f"nubia_mean: {nubia_mean}")

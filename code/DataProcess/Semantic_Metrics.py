"""
This script is designed to calculate various text similarity and quality scores between candidate texts and reference texts.
It includes functions to compute BERT scores, BLEURT scores, and Nubia scores. Each function reads files from specified 
directories, computes the scores, and saves the results either as individual JSON files or appends them to a text file.
"""

from bert_score import BERTScorer
from bleurt import score
from nubia_score import Nubia
import os
from tqdm import tqdm
import json
import random


def calBERTScore(save_folder, cand_folder, ref_folder):
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    filenames = os.listdir(cand_folder)
    for filename in tqdm(filenames):
        cand = [os.path.join(cand_folder, filename)]
        ref = [os.path.join(ref_folder, filename)]
        try:
            scorer = BERTScorer(lang="en", rescale_with_baseline=True)
            P, R, F1 = scorer.score(cand, ref)
            # Save scores in .json format
            filename = filename.replace('.txt', '.json')
            with open(os.path.join(save_folder, filename), 'w') as f:
                f.write(json.dumps(
                    {'P': P.item(), 'R': R.item(), 'F1': F1.item()}, indent=4))

        except AssertionError:
            print(f"Error with file: {filename}")
            continue


def calBLEURT(save_folder, cand_folder, ref_folder):
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    filenames = os.listdir(cand_folder)
    checkpoint = "/mnt/ly/bleurt/BLEURT-20"
    for filename in tqdm(filenames):
        with open(os.path.join(cand_folder, filename), 'r') as f:
            cand = f.read()
        cands = [cand]
        with open(os.path.join(ref_folder, filename), 'r') as f:
            ref = f.read()
        refs = [ref]
        try:
            scorer = score.BleurtScorer(checkpoint)
            scores = scorer.score(references=refs, candidates=cands)
            # Append score to a text file
            with open(os.path.join(save_folder, 'bleurt.txt'), 'a') as f:
                f.write(str(scores[0]) + '\n')

        except AssertionError:
            print(f"Error with file: {filename}")
            continue


def calNubia(save_folder, cand_folder, ref_folder):
    # Create the save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    nubia = Nubia()
    filenames = os.listdir(cand_folder)

    for filename in tqdm(filenames):
        with open(os.path.join(cand_folder, filename), 'r') as f:
            cand = f.read()
        with open(os.path.join(ref_folder, filename), 'r') as f:
            ref = f.read()
        try:
            score = nubia.score(cand, ref)
            # Append score to a text file
            with open(os.path.join(save_folder, 'nubia.txt'), 'a') as f:
                f.write(str(score) + '\n')

        except AssertionError:
            print(f"Error with file: {filename}")
            continue

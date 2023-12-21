"""
This script processes text files and uses OpenAI's GPT-4 Turbo model to generate structured responses based on the content
of the files and a predefined set of rules (crash DSL). The responses are then saved in a specified directory. It includes
retry logic to handle API rate limits and exceptions.
"""

import re
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import openai
import backoff
import time

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Read the crash DSL syntax and content
with open('DSL.txt', 'r') as f:
    crash_dsl = f.read()


def generateStructure(name):
    folder = 'original_datasets'
    filename = os.path.join(folder, name)
    with open(filename, 'r') as file:
        case_summary = file.read()

    # Decorator for exponential backoff on OpenAI API rate limits
    @backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_tries=5)
    def get_chat_response():
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are an assistant of text extraction. You need to answer me with key-value pairs based on the text. If the answer is not included in the text, you need to reply with "unmentioned"."""},
                {"role": "user", "content": "Case summary:" + case_summary + "Crash DSL:" + crash_dsl +
                    """Find out an answer in the content of the Crash DSL with the closest meaning to your answer. If there is no matching answer, keep your original answer."""},
            ],
            temperature=0.5,
            max_tokens=2048
        )
        return response.choices[0].message.content
    try:
        text = get_chat_response()
    except Exception as e:
        print("Error occurred:", e)

    folder2 = 'save_datasets'
    if not os.path.exists(folder2):
        os.makedirs(folder2)
    filename = os.path.join(folder2, name)
    with open(filename, 'w') as f:
        f.write(text)


def retry_api_call(func, name, max_retries=3, delay=5):
    for attempt in range(max_retries):
        try:
            func(name)
            return
        except Exception as e:
            print(f"Error: {e}. Retrying {attempt + 1}/{max_retries}...")
            # Wait before retrying to prevent excessive API calls
            time.sleep(delay)
    print(f"Failed to execute {func.__name__} after {max_retries} attempts.")


if __name__ == '__main__':
    flag = 0
    with open('casesummary.txt', 'r') as f:
        idlst = f.readlines()
        for id in tqdm(idlst):
            id = id.rstrip()
            flag += 1
            if (flag >= 1):
                retry_api_call(generateStructure, id)
            else:
                continue

"""
This script uses a large language model for generating structured text responses. It includes functions 
for determining the responsibility in traffic accidents and classifying the type of accident based on detailed descriptions.
The script handles model loading, application of LoRA (Low-Rank Adaptation) modifications, and generation of responses
using customized prompts. 
"""

from tqdm import tqdm
import os
from modules.models import load_model
from modules.shared import model, tokenizer
from modules.text_generation import generate_reply
# from extensions.api.util import build_parameters

from modules.chat import load_character_memoized
from modules.presets import load_preset_memoized
from threading import Lock
import modules.shared as shared
from modules.models_settings import (
    get_model_metadata,
    update_model_parameters
)
from modules.logging_colors import logger

from modules.LoRA import add_lora_to_model
import time

# In shared.py
model = None
tokenizer = None
settings = {}
generation_lock = None

# Function to build parameters for the model


def build_parameters(body, chat=False):

    generate_params = {
        'max_new_tokens': int(body.get('max_new_tokens', body.get('max_length', 200))),
        'auto_max_new_tokens': bool(body.get('auto_max_new_tokens', False)),
        'max_tokens_second': int(body.get('max_tokens_second', 0)),
        'do_sample': bool(body.get('do_sample', True)),
        'temperature': float(body.get('temperature', 0.5)),
        'temperature_last': bool(body.get('temperature_last', False)),
        'top_p': float(body.get('top_p', 1)),
        'typical_p': float(body.get('typical_p', body.get('typical', 1))),
        'epsilon_cutoff': float(body.get('epsilon_cutoff', 0)),
        'eta_cutoff': float(body.get('eta_cutoff', 0)),
        'min_p': float(body.get('min_p', 0)),
        'tfs': float(body.get('tfs', 1)),
        'top_a': float(body.get('top_a', 0)),
        'repetition_penalty': float(body.get('repetition_penalty', body.get('rep_pen', 1.1))),
        'additive_repetition_penalty': float(body.get('additive_repetition_penalty', body.get('additive_rep_pen', 0))),
        'repetition_penalty_range': int(body.get('repetition_penalty_range', 0)),
        'encoder_repetition_penalty': float(body.get('encoder_repetition_penalty', 1.0)),
        'top_k': int(body.get('top_k', 0)),
        'min_length': int(body.get('min_length', 0)),
        'no_repeat_ngram_size': int(body.get('no_repeat_ngram_size', 0)),
        'num_beams': int(body.get('num_beams', 1)),
        'penalty_alpha': float(body.get('penalty_alpha', 0)),
        'length_penalty': float(body.get('length_penalty', 1)),
        'early_stopping': bool(body.get('early_stopping', False)),
        'mirostat_mode': int(body.get('mirostat_mode', 0)),
        'mirostat_tau': float(body.get('mirostat_tau', 5)),
        'mirostat_eta': float(body.get('mirostat_eta', 0.1)),
        'grammar_string': str(body.get('grammar_string', '')),
        'guidance_scale': float(body.get('guidance_scale', 1)),
        'negative_prompt': str(body.get('negative_prompt', '')),
        'seed': int(body.get('seed', -1)),
        'add_bos_token': bool(body.get('add_bos_token', True)),
        'truncation_length': int(body.get('truncation_length', body.get('max_context_length', 2048))),
        'custom_token_bans': str(body.get('custom_token_bans', '')),
        'ban_eos_token': bool(body.get('ban_eos_token', False)),
        'skip_special_tokens': bool(body.get('skip_special_tokens', True)),
        'custom_stopping_strings': '',  # leave this blank
        'stopping_strings': body.get('stopping_strings', []),
        'presence_penalty': int(body.get('presence_penalty', 0)),
        'frequency_penalty': int(body.get('frequency_penalty', 0)),
    }

    preset_name = body.get('preset', 'None')
    if preset_name not in ['None', None, '']:
        preset = load_preset_memoized(preset_name)
        generate_params.update(preset)

    if chat:
        character = body.get('character')
        instruction_template = body.get(
            'instruction_template', shared.settings['instruction_template'])
        if str(instruction_template) == "None":
            instruction_template = "Vicuna-v1.1"
        if str(character) == "None":
            character = "Assistant"

        name1, name2, _, greeting, context, _ = load_character_memoized(character, str(
            body.get('your_name', shared.settings['name1'])), '', instruct=False)
        name1_instruct, name2_instruct, _, _, context_instruct, turn_template = load_character_memoized(
            instruction_template, '', '', instruct=True)
        generate_params.update({
            'mode': str(body.get('mode', 'chat')),
            'name1': str(body.get('name1', name1)),
            'name2': str(body.get('name2', name2)),
            'context': str(body.get('context', context)),
            'greeting': str(body.get('greeting', greeting)),
            'name1_instruct': str(body.get('name1_instruct', name1_instruct)),
            'name2_instruct': str(body.get('name2_instruct', name2_instruct)),
            'context_instruct': str(body.get('context_instruct', context_instruct)),
            'turn_template': str(body.get('turn_template', turn_template)),
            'chat-instruct_command': str(body.get('chat_instruct_command', body.get('chat-instruct_command', shared.settings['chat-instruct_command']))),
            'history': body.get('history', {'internal': [], 'visible': []})
        })

    return generate_params


# Function to initialize the model with specific settings
def initialize_model_with_settings(model_name):
    model_settings = get_model_metadata(model_name)
    shared.settings.update(model_settings)

    update_model_parameters(model_settings, initial=True)

# Function to generate a response for a given prompt


def generate_answer(prompt):
    request = {
        'prompt': prompt,
        'max_new_tokens': 200,
        # ... and so on ...
        'auto_max_new_tokens': False,
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.5,
        'temperature_last': False,
        'top_p': 0.7,
        'min_p': 0,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'presence_penalty': 0,
        'frequency_penalty': 0,
        'repetition_penalty': 1.15,
        'repetition_penalty_range': 0,
        'encoder_repetition_penalty': 1,
        'no_repeat_ngram_size': 0,
        'top_k': 20,
        'min_length': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': [],
    }

    # Get the reply
    answer = generate_answer_from_request(request)

    return answer

# Function to generate a response from a request body


def generate_answer_from_request(request_body):
    prompt = request_body['prompt']
    generate_params = build_parameters(request_body)

    stopping_strings = generate_params.pop('stopping_strings')
    generate_params['stream'] = False

    generator = generate_reply(
        prompt, generate_params, stopping_strings=stopping_strings, is_chat=False)

    answer = ''
    for a in generator:
        answer = a

    return answer

# Function to generate labels for traffic accident responsibility


def generateLabel(data_folder):
    for filename in tqdm(os.listdir(data_folder)):
        with open(os.path.join(data_folder, filename), 'r') as data_file:
            structured_data = data_file.read()
            your_system_message = "You are a helpful assistant in determining responsibility for traffic accidents in a virtual environment. Based on the given structured data, tell me which vehicle(V1,V2,Vn,etc.) is mainly responsible and then explain the reason briefly."
            user_message = structured_data
            prompt = f"<s>[INST] <<SYS>>\n{your_system_message}\n<</SYS>>\n\n{user_message} [/INST]"

            result = generate_answer(prompt)

        save_folder = 'responsibility'
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        with open(os.path.join(save_folder, filename), 'w') as label_file:
            label_file.write(result)

# Function to generate types for traffic accidents


def generateType(data_folder):
    for filename in tqdm(os.listdir(data_folder)):
        with open(os.path.join(data_folder, filename), 'r') as data_file:
            structured_data = data_file.read()
            your_system_message = """You are a helpful assistant to classify the traffic accident given detailed descriptions of various traffic scenarios. All the types are as follows: 1.Single-Vehicle Accident - Involves only one vehicle, no other entities.\n2.Backover Collision - Vehicle reverses into an object, person, or another vehicle.\n3.Rear-End Collision - One vehicle hits the back of another.\n4.Frontal Collision - Fronts of two vehicles collide head-on.\n5.Front-to-Side Collision - Front of one vehicle collides with the side of another (\"T-bone\" collision).\n6.Non-Motorized Vehicle or Pedestrian Crash - Involves bicycles, pedestrians, or other non-motorized entities.\n7.Other - This category includes other accident types not covered in the above classifications. Based on the given case summary, which type does the accident belong to? Provide the Type Number and give a brief reason.
            """
            user_message = structured_data
            prompt = f"<s>[INST] <<SYS>>\n{your_system_message}\n<</SYS>>\n\n{user_message} [/INST]"

            result = generate_answer(prompt)

        save_folder = "type"
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        with open(os.path.join(save_folder, filename), 'w') as label_file:
            label_file.write(result)


if __name__ == "__main__":
    # Model selection based on dir and model_name from models.py
    # replace with your model's name
    shared.model_name = "meta-llama_Llama-2-70b-chat-hf"

    # Initialize model with settings
    initialize_model_with_settings(shared.model_name)
    shared.model, shared.tokenizer = load_model(shared.model_name)

    # type
    shared.args.lora = ['llama70b_type-16R-128B-4E-100S']

    print(shared.args)
    add_lora_to_model(shared.args.lora)
    logger.info("Successfully applied LoRAs !")
    shared.generation_lock = Lock()

    generateType('test')

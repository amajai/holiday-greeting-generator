from app import app
from flask import render_template, request
import requests
from app import app
import os
import re
from app.variables import (
    USER_PROMPT,
    SYSTEM_PROMPT,
    KIMBA_SYSTEM_PROMPT,
    KIMBA_USER_PROMPT
)

model_name = "HuggingFaceH4/zephyr-7b-beta"
API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
headers = {"Authorization": f"Bearer {os.environ.get('TOKEN')}"}


def post_request(payload):
    """
    Sends a POST request to a specified API endpoint with the given payload.

    Parameters:
    - payload (dict): The data to be sent as the JSON payload in the POST
    request.

    Returns:
    - dict: The JSON response from the API.

    Raises:
    - requests.exceptions.RequestException: If the HTTP request encounters
    an error.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


def get_prompt_result(user_prompt, system_prompt):
    """
    Retrieves the result of a language model generation based on user and
    system prompts.

    Parameters:
    - user_prompt (str): The user's input or prompt for the language model.
    Defaults to USER_PROMPT.
    - system_prompt (str): The system's input or prompt for the language
    model. Defaults to SYSTEM_PROMPT.

    Returns:
    - str: The generated text as a result of the language model processing
    the input prompts.
    """
    input_prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_prompt}\
        </s>\n<|assistant|>"
    post_data = {
        "inputs": input_prompt
    }
    res_data = post_request(post_data)
    json_obj = res_data[0]
    if 'generated_text' in json_obj:
        res = json_obj['generated_text']
        res = res[res.find('<|assistant|>')+len('<|assistant|>'):].strip()
        return res
    else:
        return json_obj


def text_to_prompt_string(text):
    """
    Converts a given text into a formatted prompt string.

    Parameters:
    - text (str): The input text to be processed.

    Returns:
    - str: A formatted prompt string based on the input text. The function
           processes the text by identifying words and phrases, handling
           various cases such as single and multiple items, and joining them
           with appropriate separators (', ' & ' and ').
    """
    lst = re.findall(r'\w+|"[^"]*"', text)
    if len(lst) == 0:
        return ''
    if len(lst) == 1:
        return lst[0]
    if len(lst) == 2:
        return ' and '.join(lst)
    return ', '.join(lst[:-1]) + ' and ' + lst[-1]


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handles the main route of the web application.

    If a POST request is received, it processes the form data, generates a
    text prompt based on the input, and returns the generated output.

    Returns:
    - str or JSON: The generated text output if successful, or a JSON
    response with an error message.
    """
    if request.method == "POST":
        holiday = request.form['holiday']
        select_type = request.form['select_type']
        receiver_name = request.form['receiver_name'].lower().strip()
        if not receiver_name == 'kimba':
            receiver_name = f"with the name {receiver_name}"\
                if receiver_name else ''

            receiver_location = request.form['receiver_location']
            receiver_location = f"in {receiver_location}" \
                if receiver_location else ''

            select_relation = request.form['select_relation']

            keywords_string = text_to_prompt_string(request.form['keywords'])
            keywords = f". Make mention or highlight on {keywords_string}" \
                if keywords_string else ''

            sentiments_text = text_to_prompt_string(request.form['sentiments'])
            sentiments = f". The greeting tone should be {sentiments_text}" \
                if sentiments_text else ''

            user_prompt = USER_PROMPT.format(
                    holiday=holiday,
                    receiver_name=receiver_name,
                    receiver_location=receiver_location,
                    select_relation=select_relation,
                    select_type=select_type,
                    keywords=keywords,
                    sentiments=sentiments,
                )
            output = get_prompt_result(user_prompt, SYSTEM_PROMPT)
        else:
            user_prompt = KIMBA_USER_PROMPT.format(
                    holiday=holiday,
                    select_type=select_type,
                )
            output = get_prompt_result(user_prompt, KIMBA_SYSTEM_PROMPT)
        return output
    return render_template("index.html")

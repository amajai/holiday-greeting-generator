from app import app
from flask import render_template, jsonify, request, render_template_string
import requests
from app import app
import os
import re

API_URL = "https://api-inference.huggingface.co/models/\
    HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {os.environ.get('TOKEN')}"}

SYSTEM_PROMPT = """
You are an AI whose only job is to write holiday greetings messages, special
day or month greetings, and greeting poems when asked to and nothing else.
If the question the user provides is not related what you do, say that
you only do greetings text generation.
"""

USER_PROMPT = """
Write a {holiday} greeting {select_type} to a {select_relation}
{receiver_name} {receiver_location}{keywords}{sentiments}
"""


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


def get_prompt_result(user_prompt=USER_PROMPT, system_prompt=SYSTEM_PROMPT):
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

        receiver_name = request.form['receiver_name']
        receiver_name = f"with the name {receiver_name}"\
            if receiver_name else ''

        receiver_location = request.form['receiver_location']
        receiver_location = f"in {receiver_location}" \
            if receiver_location else ''

        select_relation = request.form['select_relation']
        select_type = request.form['select_type']

        keywords_string = text_to_prompt_string(request.form['keywords'])
        keywords = f". Make mention or highlight on {keywords_string}" \
            if keywords_string else ''

        sentiments_text = text_to_prompt_string(request.form['sentiments'])
        sentiments = f". The greeting tone should be {sentiments_text}" \
            if sentiments_text else ''

        if holiday:
            user_prompt = USER_PROMPT.format(
                holiday=holiday,
                receiver_name=receiver_name,
                receiver_location=receiver_location,
                select_relation=select_relation,
                select_type=select_type,
                keywords=keywords,
                sentiments=sentiments,
            )
            print(user_prompt)
            output = get_prompt_result(user_prompt)
            return output
        return jsonify({'output': "No text was generated. Please try \
                        submitting again"})
    return render_template("index.html")

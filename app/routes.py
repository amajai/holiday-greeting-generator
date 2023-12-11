from app import app
from flask import render_template, jsonify, request, render_template_string
import requests
from app import app
import time
import os
import json
import re

API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
headers = {"Authorization": f"Bearer {os.environ.get('TOKEN')}"}

SYSTEM_PROMPT = """
You are an AI whose only job is to write holiday greetings messages, special
day or month greetings, and greeting poems when asked to and nothing else.
If the question the user provides is not related what you do, say that
you only do greetings text generation.
"""

USER_PROMPT = """
Write a {holiday} greeting {select_type} to a {select_relation} 
{receiver_name} in {receiver_location}. Highlight 
on the {keywords}
"""

def post_request(payload):
    """
    Perform a POST request to the Hugging Face Inference API with the provided payload.
    """
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def build_input_prompt(user_prompt, system_prompt):
    """
    Constructs the input prompt string.
    """
    input_prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_prompt}</s>\n<|assistant|>\n"
    return input_prompt

def get_prompt_result(user_prompt=USER_PROMPT, system_prompt=SYSTEM_PROMPT):
    input_prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{user_prompt}</s>\n<|assistant|>"
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

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        holiday = request.form['holiday']
        receiver_name = request.form['receiver_name']
        receiver_name = f"with the name {receiver_name}" if receiver_name else ''
        receiver_location = request.form['receiver_location']
        select_relation = request.form['select_relation']
        select_type = request.form['select_type']
        keywords = request.form['keywords']
        keywords = ' and '.join(re.findall(r'\w+|"[^"]*"', keywords))

        if holiday:
            user_prompt = USER_PROMPT.format(
                holiday=holiday,
                receiver_name=receiver_name,
                receiver_location=receiver_location,
                select_relation=select_relation,
                select_type=select_type,
                keywords=keywords
            )
            output = get_prompt_result(user_prompt)
            return output
        return jsonify({'output' : "Try resubmitting the prompt again"})
    return render_template("index.html")

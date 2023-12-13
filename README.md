# Holiday Greeting Generator App
![Animation2](https://github.com/amajai/holiday-greeting-generator/assets/44467524/020f425f-4985-4f38-9485-f5e8f98b43aa)

Link: https://holiday-greeting-generator.onrender.com

An Artificial Intelligence (AI) text generation application that lets you generate personalized holiday greetings for various occasions! Whether it's Christmas, New Year, Eid, or any other special day, this app is here to help you spread joy and warmth with customized greetings. It is powered by a Large Language Model (LLM) called Zephyr-7B-β.

## Overview
The App leverages Zephyr-7B-β, a fine-tuned model in the Zephyr series, designed to act as a helpful assistant. Trained on a mix of publicly available and synthetic datasets using Direct Preference Optimization (DPO), this language model brings a touch of personalization to your holiday greetings.

## Features
1. Holiday Selection: Choose from a variety of holidays, occasions, special days/weeks/months to tailor your greeting.
1. Optional Inputs: Personalize your greeting further by providing optional details.

## Sample Usage
The greeting generation process involves seven input parameters, with one being mandatory while the remaining six are optional. An illustrative example is provided below for reference:
### Required Input:
- Holiday: New Year
### Optional Inputs:
- Receiver Name: John Doe
- Receiver Location: Abuja
- Sentiments: Warm joyful
- Relation: Friend
- Greeting Type: Formal
- Keywords: Peace, Happiness, Celebration

## Technologies Used
1. Flask - The backend is powered by Flask, providing a robust and scalable foundation.
1. JavaScript and jQuery - Enhance user interactivity and dynamically update the page without reloading.
1. Ajax - Asynchronous communication with the server to fetch and display data in real-time.
1. Bulma for CSS - Stylish and responsive design using Bulma, making the app visually appealing. It's simple to work with.

## Citation
```
@misc{tunstall2023zephyr,
      title={Zephyr: Direct Distillation of LM Alignment}, 
      author={Lewis Tunstall and Edward Beeching and Nathan Lambert and Nazneen Rajani and Kashif Rasul and Younes Belkada and Shengyi Huang and Leandro von Werra and Clémentine Fourrier and Nathan Habib and Nathan Sarrazin and Omar Sanseviero and Alexander M. Rush and Thomas Wolf},
      year={2023},
      eprint={2310.16944},
      archivePrefix={arXiv},
      primaryClass={cs.LG}
}
```

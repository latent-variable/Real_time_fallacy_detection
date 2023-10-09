import json
from random import shuffle
 
INSTRUCTION = """Note: The following debate transcript may contain imperfections, such as multiple people talking over each other and question being asked by indivudals or moderator. Please take this into consideration when analyzing the text.
Analyze the following debate excerpt for logical fallacies and format your response by starting with the name of the fallacy, followed by a brief justification.
If the statement is factual or logical, or if no argument is present, state so explicitly. Avoid covering the same points from the Last Debate Excerpt.

Debate Excerpt: 
"""


def get_few_shot_examples(file_name=r'Data/data.json', N=5):
    try:
        with open(file_name, "r") as json_file:
            all_data = json.load(json_file)
    except FileNotFoundError:
        return "No data available."
    
    shuffle(all_data)
    # Get last N examples from the JSON data
    last_n_examples = all_data[-N:]
    
    # Generate the few-shot string
    few_shot_string = ""
    for example in last_n_examples:
        few_shot_string += f"Debate Excerpt: \"{example['transcript']}\"\n"
        few_shot_string += f"{example['response']}\n\n"
    
    return few_shot_string


def get_prompt(transcript, last_responce):
    few_shot = get_few_shot_examples(file_name=r'Data/data.json', N=5)
    
    prompt = f'{few_shot}\n{last_responce}\n\n{INSTRUCTION}\n\"{transcript}\"'
    return prompt

if __name__=="__main__":
    pass
    # update_json_file( file_name=r'Data/data.json')
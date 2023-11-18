import json
from random import shuffle
 
INSTRUCTION = """Real-Time Debate Analysis

Note: You are about to analyze a live debate segment. The transcript provided is generated in real-time and may contain imperfections, such as overlapping speech and interruptions by the moderator or other participants. Please consider these factors in your analysis.

Objective: Your task is to critically evaluate the arguments presented in the debate. Focus on identifying any logical inconsistencies, factual errors, or rhetorical weaknesses. Use the accompanying image to determine who the speaker is.

Guidelines for Analysis:

Be concise and direct in your response, as the analysis needs to align with the real-time nature of the debate.
When referencing speakers, rely on the provided image for accurate identification and include their name to minimize confusion.
Keep in mind that the debate environment is dynamic; arguments may evolve quickly, and interruptions are common.
Response should NOT exceed 3 sentences. Avoid qualifiers or additional context. Do not provide disclaimers!
Debate Excerpt:
"""

def get_few_shot_examples(file_name=r'Data/data.json', N=5):
    try:
        with open(file_name, "r") as json_file:
            all_data = json.load(json_file)
    except FileNotFoundError:
        return "No data available."
    if N <= 0:
        return ""
    
    shuffle(all_data)
    # Get last N examples from the JSON data
    last_n_examples = all_data[-N:]
    
    # Generate the few-shot string
    few_shot_string = ""
    for example in last_n_examples:
        few_shot_string += f"Debate Excerpt: \"{example['transcript']}\"\n"
        few_shot_string += f"{example['response']}\n\n"
    
    return few_shot_string


def get_prompt(transcript):
    few_shot = get_few_shot_examples(file_name=r'Data/data.json', N=0)
    
    prompt = f'{few_shot}\n{INSTRUCTION}\n\"{transcript}\"'
    return prompt

if __name__=="__main__":
    pass
    # update_json_file( file_name=r'Data/data.json')
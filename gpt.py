import json
import openai  # Assuming you've installed the OpenAI Python package
from local_llm import local_llm_call
from prompt import get_prompt, INSTRUCTION

# Function to read API key from a file
def read_api_key(file_path = r'./api_key.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
# Initialize GPT-3 API Client
openai.api_key = read_api_key()
LAST_RESPONCE = ''

def save_to_json_file(transcript, instruction, response, file_name=r'Data/data.json'):
    # Prepare new data entry
    
    new_data = {
        "transcript":transcript,
        "prompt": instruction,
        "response": response
    }
    # Read existing data
    try:
        with open(file_name, "r") as json_file:
            all_data = json.load(json_file)
    except FileNotFoundError:
        all_data = []
    
    # Append new data
    all_data.append(new_data)

    # Write updated data back to file
    with open(file_name, "w") as json_file:
        json.dump(all_data, json_file)


def fallacy_classification(transcript, use_gpt = False):
    global LAST_RESPONCE
    # Create a more nuanced prompt for the LLM
    prompt = get_prompt(transcript, LAST_RESPONCE)

    # Call ChatGPT API for fallacy detection or other tasks
    if not use_gpt:
        print('Prompting Local LLM')
        llm_response  = local_llm_call(prompt)
        if 'ß' in llm_response:
            llm_response = ''
        # print(f'{prompt}\n\n {llm_response}')
    else:
        print(f'Prompting {use_gpt}')
        response = openai.ChatCompletion.create(
            model= use_gpt,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
        )
    
        llm_response  = response['choices'][0]['message']['content'].strip() # Extract and clean the output text
         # print("GPT-3 Output:", llm_response)

    # Store the last response data
    LAST_RESPONCE = f'Last Debate Excerpt: {transcript}\n {llm_response}'

    if use_gpt:
        save_to_json_file(transcript, INSTRUCTION, llm_response)

    return llm_response




    
if __name__=="__main__":
    save_to_json_file("transcript", "prompt", "response",  "few_shot_examples")
import openai  # Assuming you've installed the OpenAI Python package


# Function to read API key from a file
def read_api_key(file_path = r'./api_key.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()
    
# Initialize GPT-3 API Client
openai.api_key = read_api_key()


def fallacy_classification(text):
     # Create a more nuanced prompt for ChatGPT
    prompt = f"""
    During a political debate, the following statement was made:
    "{text}"
    
    Please identify any logical fallacies present, such as Strawman, Ad Hominem, Slippery Slope, etc. Provide a brief justification for why it's a fallacy. If no argument has been made or if the statement is factual and logical, please state so explicitly.

    Provide a single sentence response, and the name of the fallacy.
    """
   
    # Call ChatGPT API for fallacy detection or other tasks
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    
    gpt3_output = response['choices'][0]['message']['content'].strip() # Extract and clean the output text
    print("GPT-3 Output:", gpt3_output)
    return gpt3_output


def is_a_complete_statement(text):
     
    # Create a prompt for ChatGPT to assess the completeness of the statement
    prompt = f"""
    Analyze the following statement from a debate to determine if a least one complete arguments is present within the text:
    "{text}"

    Only respond with 'Contains a complete argument' or 'The statement is incomplete'.
    """
    
    # Call ChatGPT API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        
    )
    
    gpt3_output = response['choices'][0]['message']['content'].strip()
    print("GPT-3 Output:", gpt3_output)

    # Further logic based on GPT-3 output
    if " complete" in gpt3_output:
        print("The statement is complete.")
        return True
        # Proceed with fallacy detection or other tasks
    elif "incompleted" in gpt3_output:
        print("The statement is incomplete.")
        return False
        # Wait for more of the statement to be transcribed
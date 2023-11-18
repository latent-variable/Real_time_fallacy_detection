import io
import json
from local_llm import local_llm_call
from prompt import get_prompt, INSTRUCTION
import pyaudio
from pydub import AudioSegment
from openai import OpenAI


# Function to read API key from a file
def read_api_key(file_path = r'./api_key.txt'):
    with open(file_path, 'r') as file:
        return file.read().strip()
    

pyaudio.PyAudio()

# Initialize API Client
api_key = read_api_key()
client = OpenAI(api_key = read_api_key())
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


def text_fallacy_classification(formatted_base64_image, transcript):
    # Create a more nuanced prompt for the LLM
    prompt = get_prompt(transcript)
    

    # Call ChatGPT API for fallacy detection or other tasks
    print(f'Prompting gpt-4 with vision...')
   

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        response = client.chat.completions.create(
            model ="gpt-4",
            messages =  [
                {"role": "system", 
                 "content":[{
                     "type": "text", 
                     "text":"You are an advanced AI assistant designed to impartially analyze political arguments and debates. Using real-time detection of logical fallacies and data-driven insights, you aid in enhancing the public's understanding of political discourse. Your objective analysis supports users in making informed decisions about political candidates."
                     }],
                }, 
                {  "role": "user",
                    "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                   
                    ]
                }
            ],
            max_tokens = 100
        )
      

 
        llm_response  = response.choices[0].message.content.strip() # Extract and clean the output text
        print("GPT-Vision Output:", llm_response)


    except Exception as e:
        print(e)
        llm_response = "No reponse"
    return llm_response


def openAI_TTS(text, filename='tts/audio.mp3'):
    response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=text,
                )
    response.stream_to_file(filename)
    return filename

def openAI_STT(audio_buffer):
  # Assuming audio_buffer is already a BytesIO object with audio data

    # Reset buffer's position to the beginning
    audio_buffer.seek(0)

    transcript = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_buffer
        )
    text = transcript['text']

    return text

if __name__=="__main__":
    save_to_json_file("transcript", "prompt", "response",  "few_shot_examples")
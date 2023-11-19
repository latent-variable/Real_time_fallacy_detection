import io
import json
from prompt import get_prompt, SYSTEM_Commentary
import pyaudio
from pydub import AudioSegment
from openai import OpenAI

from audio import  CHANNELS, RATE
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
        response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages =  [
                {"role": "system", 
                 "content":[{
                     "type": "text", 
                     "text":SYSTEM_Commentary
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


def openAI_TTS(text, filename='audio/tts_audio.wav'):
    response = client.audio.speech.create(
                    model="tts-1",
                    voice="onyx",
                    input=text,
                )
    response.stream_to_file(filename)
    return filename

def openAI_STT(audio_bytearray):

    # Convert the bytearray to an AudioSegment
    audio = AudioSegment.from_raw(io.BytesIO(audio_bytearray), format="raw", frame_rate=RATE, channels=CHANNELS, sample_width=2)

    # Convert the audio to a supported format (e.g., mp3)
    buffer = io.BytesIO()
    audio.export(buffer, format="mp3")
    buffer.seek(0)

    # Debug: Save the buffer to a file to check the conversion
    with open("audio/sst_audio.mp3", "wb") as f:
        f.write(buffer.getvalue())

    audio_file= open("audio/sst_audio.mp3", "rb")
    transcription_object = client.audio.transcriptions.create(
                                model="whisper-1", 
                                file=audio_file
                                )

     # Access the transcription text
    try:
        text = transcription_object.text
    except AttributeError:
        # Handle the case where 'text' attribute does not exist
        # This might involve logging an error or returning a default value
        text = ""

    return text

if __name__=="__main__":
    save_to_json_file("transcript", "prompt", "response",  "few_shot_examples")
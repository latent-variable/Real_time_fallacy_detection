import wave
import time
import torch 
import pyaudio
import threading
import numpy as np
from collections import deque

from audio import find_input_device_index, find_output_device_index
from audio import FORMAT, CHANNELS, RATE, CHUNK
from openai_wrapper import openAI_STT

# Global variables 
WHISPER_TEXTS = []
audio_buffer_lock = threading.Lock()
# Global variables for running average
running_avg_buffer = deque(maxlen=30)  # Adjust maxlen to your preference
average_threshold_ratio = 0.5  # Adjust based on experimentation

audio = pyaudio.PyAudio()
input_device_index = find_input_device_index()
input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                              input=True, frames_per_buffer=CHUNK,
                              input_device_index=input_device_index)

print('Input device index:', input_device_index)
output_device_index = find_output_device_index()
output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                               output=True, frames_per_buffer=CHUNK,
                               output_device_index=output_device_index)
    
print('Output device index:', output_device_index)

def save_byte_buffer(audio, audio_buffer, byte_size_chunk):
    # Save to a WAV file for verification
    with wave.open("audio_chunk.wav", "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(audio.get_sample_size(FORMAT))
        wav_file.setframerate(RATE)
        wav_file.writeframes(audio_buffer[:byte_size_chunk])


def get_audio_tensor(audio_buffer):
    audio_buffer_np = np.frombuffer(audio_buffer, dtype=np.int16)  
    # Convert to float32
    audio_float32 = audio_buffer_np.astype(np.float32)
    # Normalize
    audio_normalized = audio_float32 / 32768.0
    # Convert to Torch tensor
    audio_tensor = torch.from_numpy(audio_normalized)
    # Optionally move to GPU
    if torch.cuda.is_available():
        audio_tensor = audio_tensor.cuda()

    return audio_tensor

def transcription_callback(new_text):
    global WHISPER_TEXTS  # Declare the list as global so we can append to it
    cleaned_text = new_text.strip()
    if len(cleaned_text):
        # print('Adding trancription')
        WHISPER_TEXTS.append(cleaned_text + '\n')

    
def transcription(whs_model,  audio_buffer, callback):
    
    try:
        trascribed_text = ''
        if whs_model: # Local transcription 
            with audio_buffer_lock:
                # Change dtype based on your bit depth
                audio_tensor = get_audio_tensor(audio_buffer)
            transcription = whs_model.transcribe(audio_tensor, language='en', fp16=torch.cuda.is_available())
            trascribed_text = transcription['text']
        else: # using openAIs API
            trascribed_text = openAI_STT(audio_buffer)

        # Process the transcription (e.g., fallacy detection)
        callback(trascribed_text)
    except Exception as e:
        print(e)
        print('Skipping transcription ..')

def update_running_average(new_value):
    running_avg_buffer.append(new_value)
    return np.mean(running_avg_buffer)

def is_silence(audio_data, base_threshold=150):
    """Check if the given audio data represents silence based on running average."""
    current_level = np.abs(audio_data).mean()
    running_avg = update_running_average(current_level)

    if running_avg < base_threshold: # this might indicate just silence 
        return False
    
    dynamic_threshold = running_avg * average_threshold_ratio
    threshold = max(dynamic_threshold, base_threshold)

    # print(f"Current Level: {current_level}, Running Avg: {running_avg}, Threshold: {threshold}")

    return current_level < threshold

def continuous_audio_transcription(whs_model, stop_event):
    print('Continuous audio transcription...')
    global input_stream, output_stream
    # Initialize empty audio buffer
    audio_buffer = bytearray()
    seconds = 6
    data_byte_size = 32_000 # 1 second of data 
    byte_size_chunk = data_byte_size * seconds 
    silence_counter = 0 
    while not stop_event.is_set():  # Assuming you have a stopping condition
        
        # Read audio chunk
        audio_chunk = input_stream.read(CHUNK)
        # Check if the chunk is silence
        audio_data = np.frombuffer(audio_chunk, dtype=np.int16)
        if is_silence(audio_data):
            silence_counter += 1
        else:
            silence_counter = 0

        # Write audio chunk to output device
        output_stream.write(audio_chunk)

        # Append to audio buffer
        with audio_buffer_lock:
            audio_buffer += audio_chunk
        
        # print('silence_counter', silence_counter)
        # When buffer reaches a certain size, or a silence break is detected send for transcription
        if silence_counter > 3: 
                if (len(audio_buffer) >=  byte_size_chunk  ):
                    silence_counter = 0  # Reset the counter
                    transcribe_thread = threading.Thread(target=transcription, args=(whs_model, audio_buffer, transcription_callback))
                    transcribe_thread.start()
                    with audio_buffer_lock:
                        audio_buffer = bytearray()  # Clear the buffer
        else:
            with audio_buffer_lock:
                # Append to audio buffer
                audio_buffer += audio_chunk

            
    print('Exiting')
    
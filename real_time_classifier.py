import wave
import torch 
import pyaudio
import threading
import numpy as np

from audio import find_input_device_index, find_output_device_index
from audio import FORMAT, CHANNELS, RATE, CHUNK
from gpt import fallacy_classification, is_a_complete_statement

# Global variables 
WHISPER_TEXTS = []
GPT_TEXTS = []
MAX_SEGEMENTS = 10
audio_buffer_lock = threading.Lock()

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

def get_last_segments(text_list):
    # Get the last N segments from the list
    last_n_segments = text_list[-MAX_SEGEMENTS:]
     # Combine them into a single string
    combined_text = " ".join(last_n_segments)
    return combined_text

def transcription_callback(new_text):
    global WHISPER_TEXTS, GPT_TEXTS  # Declare the list as global so we can append to it
    WHISPER_TEXTS.append(new_text)

    text = get_last_segments( WHISPER_TEXTS )
    # print("\nTranscribed Text:", text)
   
    # Call chatgpt for fallacy classification
    if len(WHISPER_TEXTS) % 8 == 0:
       # if is_a_complete_statement(text):
        GPT_TEXTS.append(fallacy_classification(text))

    # Get the last segments from the list
    # WHISPER_TEXTS = WHISPER_TEXTS[-MAX_SEGEMENTS:]

  

def transcription(whs_model,  audio_tensor,  callback):
    # Model call to transcribe the data
    try:
        transcription = whs_model.transcribe(audio_tensor, language='en', fp16=torch.cuda.is_available())
        # Process the transcription (e.g., fallacy detection)
        callback(transcription['text'])
    except Exception as e:
        print('Skipping transcription ..')

def is_silence(audio_data, threshold=50):
    """Check if the given audio data represents silence."""
    
    if np.abs(audio_data).mean() < threshold:
        
        return True
    return False

def continuous_audio_transcription_and_classification(whs_model, stop_event):
    print('Continuous audio transcription...')
    # Initialize PyAudio and open a stream
    audio = pyaudio.PyAudio()
    input_device_index = find_input_device_index()
    output_device_index = find_output_device_index()
     # Input Stream
    input_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, 
                              input=True, frames_per_buffer=CHUNK,
                              input_device_index=input_device_index)

    # Output Stream
    output_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                               output=True, frames_per_buffer=CHUNK,
                               output_device_index=output_device_index)

    # Initialize empty audio buffer
    audio_buffer = bytearray()
    seconds = 10 
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

        # When buffer reaches a certain size, or a silence break is detected send for transcription
        if silence_counter > 5 or (len(audio_buffer) >= byte_size_chunk):
                if (len(audio_buffer) >=  data_byte_size * 2  ):
                    silence_counter = 0  # Reset the counter
                    # print('len(audio_buffer)', len(audio_buffer))
                    # Create a new thread for transcription
                    # save_byte_buffer(audio, audio_buffer, byte_size_chunk)
                    with audio_buffer_lock:
                        # Change dtype based on your bit depth
                        audio_tensor = get_audio_tensor(audio_buffer)
                    transcribe_thread = threading.Thread(target=transcription, args=(whs_model, audio_tensor, transcription_callback))
                    transcribe_thread.start()
                    with audio_buffer_lock:
                        audio_buffer = bytearray()  # Clear the buffer
        else:
            with audio_buffer_lock:
                # Append to audio buffer
                audio_buffer += audio_chunk

            
    print('Exiting')
    
                
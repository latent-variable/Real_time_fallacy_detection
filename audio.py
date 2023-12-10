import wave
import pyaudio
import configparser
import librosa
import soundfile as sf
from pydub import AudioSegment

# Audio format Parameters for whisper
FORMAT = pyaudio.paInt16  # 16-bit depth
CHANNELS = 1  # Mono
RATE = 16000  # 16kHz
CHUNK = 1024  # Smaller chunks might reduce latency
RECORD_SECONDS = 30  # 30 seconds to match Whisper's expected segment length

def print_input_devices():
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    print("Input devices:")
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device ID ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

def print_output_devices():
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # Get total number of devices
    num_devices = p.get_device_count()
    # Loop through and print device info
    print("Output devices:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxOutputChannels'] > 0:  # Output device
            print(f"Index: {i}, Name: {device_info['name']}, Channels: {device_info['maxOutputChannels']}")

    # Terminate PyAudio
    p.terminate()


def find_output_device_index():
    
    # Initialize ConfigParser
    config = configparser.ConfigParser()

    # Read settings.ini file
    config.read('settings.ini')
    # Get values
    device_output_name = config.get('Audio Settings', 'device_output_name')

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # Get total number of devices
    num_devices = p.get_device_count()
    # Loop through and print device info
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info.get('name')

        # Search for VB-Audio in the device name
        if device_output_name in device_name:
            return i
    
    # If no device is found, assert False
    assert False, "Could not find output device. Check settings.ini file"
   

def find_input_device_index():
    
    # Initialize ConfigParser
    config = configparser.ConfigParser()

    # Read settings.ini file
    config.read('settings.ini')
    # Get values
    device_input_name = config.get('Audio Settings', 'device_input_name')
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        
        # Search for VB-Audio in the device name
        if device_input_name in device_name:
            return i
    
    # If no device is found, assert False
    assert False, "Could not find input device. Check settings.ini file"


def record_short_audio():

    # Change this to the index of the device you want to use
    # Default recoding devie uses vb audio 
    input_device_index = find_input_device_index()

    # Initialize PyAudio and start recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK, input_device_index=input_device_index)

    print("Recording...")
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording")

    # Stop the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the audio
    save_audio_frames(audio, frames)


def save_audio_frames(audio, frames):
    WAVE_OUTPUT_FILENAME = "audio.wav"
    # Save the recording as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved as {WAVE_OUTPUT_FILENAME}")


def change_playback_speed(audio_file, speed=1.25):
       # Load the audio file with librosa
    y, sr = librosa.load(audio_file, sr=None)
    
    # Use librosa's effects.time_stretch for time-stretching without pitch change
    y_fast = librosa.effects.time_stretch(y, rate=speed)
    
    # Write the altered audio back to a file
    sf.write(audio_file, y_fast, sr)
    
    return audio_file

def play_audio(filename):

     # Open the audio file
    wf = wave.open(filename, 'rb')
    
    # Create a PyAudio instance
    p = pyaudio.PyAudio()
    
    # Open an output stream
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    # Read data in chunks
    data = wf.readframes(1024)
    
    # Play the audio file
    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(1024)
    
    # Close the stream
    stream.stop_stream()
    stream.close()
    
    # Terminate the PyAudio instance
    p.terminate()



if __name__=='__main__':
    print_input_devices()
    print_output_devices()

    # record_short_audio()

import wave
import pyaudio


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

def find_output_device_index(dname="Headphones (2- Razer Nari"):
    # Initialize PyAudio
    p = pyaudio.PyAudio()
    # Get total number of devices
    num_devices = p.get_device_count()
    # Loop through and print device info
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        device_name = device_info.get('name')

        # Search for VB-Audio in the device name
        if dname in device_name:
            return i
   
    return None

def find_input_device_index(iname="VB-Audio"):
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    
    for i in range(0, numdevices):
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        device_name = device_info.get('name')
        
        # Search for VB-Audio in the device name
        if iname in device_name:
            return i
    
    # Return None if not found
    return None

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


if __name__=='__main__':
    record_short_audio()
    # print_input_devices()
    # print_output_devices()
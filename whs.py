import whisper
import configparser

def get_model_options():
    models = whisper.available_models()
    print('Available models: ', ''.join(models))

def load_model():
    # Selected and load from the list of available models that can fit in your system

     # Initialize ConfigParser
    config = configparser.ConfigParser()

    # Read settings.ini file
    config.read('settings.ini')
    # Get values
    whisper_model = config.get('Local Wisper Settings', 'whisper_model')

    # Load the model
    print(f'Loading the {whisper_model} model...')
    model = whisper.load_model(whisper_model)
    print('Model loaded')
    
    return model

def test_whisper(file='audio_chunk.wav'):
    model = load_model()
    transcription = model.transcribe(file)
    print(transcription['text'])
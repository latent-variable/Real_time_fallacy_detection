import whisper

def get_model_options():
    models = whisper.available_models()
    print('Available models: ', ''.join(models))

def load_model():
    # Selected and load from the list of available models that can fit in your system
    model = "large-v2"
    # model = "medium.en"
    print(f'Loading the {model} model...')
    model = whisper.load_model(model)
    print('Model loaded')
    return model

def test_whisper(file='audio_chunk.wav'):
    model = load_model()
    transcription = model.transcribe(file)
    print(transcription['text'])
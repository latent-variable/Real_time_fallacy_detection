
# Real-time Fallacy Detection

## Overview

This project aims to perform real-time fallacy detection during events like presidential debates. It uses the (Whisper)[https://github.com/openai/whisper] for audio transcription and the OpenAI ChatGPT API for natural language understanding and fallacy classification.

## Features

- **Real-time Audio Transcription**: Uses OpenAI's Whisper ASR model for accurate real-time transcription.
- **Fallacy Detection**: Utilizes OpenAI's ChatGPT to classify and identify fallacies in real-time.
- **Overlay Display**: Provides a transparent overlay display to show both the transcription and fallacy detection results.

## Dependencies

- PyQt5
- PyAudio
- OpenAI's Whisper ASR and ChatGPT API
- (any other dependencies)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/your_username/real-time-fallacy-detection.git
    ```
2. Navigate to the project directory:
    ```
    cd real-time-fallacy-detection
    ```
3. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
4. Installing VB-AUDIO, to forward audio ouput as an input device (*Optional) 
    (VB-Audio)[https://vb-audio.com/Cable/]
## Usage

Run the main script to start the application:

```
python main.py
```

The application will display an overlay with two sections:

- **Top Box**: Displays the real-time transcription from the Whisper API.
- **Bottom Box**: Displays the fallacy classification from ChatGPT.

Press the `Esc` key to close the application.

## Configuration

You can configure the audio parameters and API keys in the `config.py` file.

## License

This project is licensed under the MIT License.

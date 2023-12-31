
# Real-time Fallacy Detection

## Overview

This project aims to perform real-time fallacy detection during events like presidential debates. It uses the [Whisper](https://github.com/openai/whisper) for audio transcription.  For natural language understanding and fallacy classification you have the option to use the OpenAI ChatGPT API or a local LLM through the [text-generation-webui](https://github.com/oobabooga/text-generation-webui). I was able to run both whisper with the [IconicAI_NeuralHermes-2.5-Mistral-7B-exl2-5bpw](https://huggingface.co/IconicAI/NeuralHermes-2.5-Mistral-7B-exl2-5bpw) on a laptop with 3080TI 16GB of VRAM.
![Alt text](img/Fallacy_classification.PNG)
[Watch Video](https://www.youtube.com/watch?v=I9ScRL_10So)

## Features

- **Real-time Audio Transcription**: Uses OpenAI's Whisper ASR model for accurate real-time transcription locally or through API access.
- **Fallacy Detection**: Utilizes OpenAI's ChatGPT to classify and identify fallacies in real-time.
- **Overlay Display**: Provides a transparent overlay display to show both the transcription and fallacy detection results.
- **Text analysis**: using GPT-3/4 or local LLM. 


## Dependencies
- Anaconda
- PyQt5 - Overlay
- PyAudio - Audio processing
- openai-whisper - ASR
- openai - ChatGPT API
- torch with cuda, for real time transtriction 
- Have the text-generation-webui running with the API flag 

## Installation
I build the application using Anaconda with python 3.9 on windows 

1. Clone the repository:
    ```
    git clone https://github.com/latent-variable/Real_time_fallacy_detection.git
    ```
2. Navigate to the project directory:
    ```
    cd real-time-fallacy-detection
    ```
3. Create a conda environment:
    ```
    conda create --name rtfd python=3.9
    ```
4. Activate the created environment:
    ```
    conda activate rtfd
    ```
5. Install the required packages:
    ```
    pip install -r requirements.txt
    ```
6. (Optional) Install the required packages to run whisper locally:
    ```
    pip install -r requirements_local_whisper.txt
    ```
7. Installing [VB-Audio](https://vb-audio.com/Cable/), to forward audio ouput as an input device (*Optional, but I don't know how to redirect audio otherwise)

## Usage

Run the main script to start the application:
```
python main.py 
optional arguments:
  -h, --help     show this help message and exit
  --auto         Automatically get commentary
  --api_whisper  Run whisper through api instead of locally
  --api_gpt      Will use use gpt api otherwise, by defualt will use a local LLM through the text-generation-webui API
```

If you plan to use your local LLM, please have the text-generation-webui running with the --api flag

**Note**: The application routes the audio to VB-AUDIO for processing and then redirects it back to the user for playback. 

## Arguments
--use_gpt(3/4): Use this flag to toggle between  ChatGPT with or without GPT4. Default is to use local LLM.

## Display
The application will display an overlay with two sections:

- **Top Box**: Displays the fallacy classification from ChatGPT.
- **Bottom Box**: Displays the real-time transcription from the Whisper API.

Press the `Esc` key to close the application.

## Configuration
[Audio Settings]
You can configure the audio input and outsource in the `settings.ini`.
- **device_input_name = VB-Audio**  <- must have 
- **device_output_name = Headphones (2- Razer** <- replace with your own 
*Note: when the application loads if will redirect the audio back to the output device
![Alt text](img/audio_selection.png)

[Local LLM Settings]
- **instruction_template = mistral-openorca** <- replace with the model specific template
*Note: this is a custom template, which you will likely note have in your text-generation-webui


Rename the `api_key.txt.template` to `api_key.txt` and add your OpenAI API key to it.

## License

This project is licensed under the MIT License.

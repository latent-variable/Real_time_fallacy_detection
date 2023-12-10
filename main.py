
import argparse
from whs import load_model
from overlay import launch_overlay


def get_inputs():
    # Create the parser
    parser = argparse.ArgumentParser(description='Toggle between Local LLM and ChatGPT.')
    parser.add_argument('--auto', action='store_true', default=False, help='Automatically get commentary')
    parser.add_argument('--api_whisper', action='store_true', default=False, help='Run whisper through api instead of locally')
    parser.add_argument('--api_gpt', action='store_true', default=False, help='Will use use gpt api otherwise, by defualt will use a local LLM through the text-generation-webui API')

    
    # Parse the arguments
    args = parser.parse_args()

    # Extract the specific arguments
    auto = args.auto
    api_whisper = args.api_whisper
    api_gpt = args.api_gpt

    return auto, api_whisper, api_gpt

def get_whisper_model(api_whisper):
    # Load the model
    # If api_whisper is true, then we will not load the model
    # This is because we will use the api instead
    if api_whisper:
        whs_model = None
    else:
        # Load the model
        whs_model = load_model()
   
    return whs_model

def main(whs_model, auto):

    # Launch the GUI in the main thread
    launch_overlay(whs_model, auto )
    

if __name__ == "__main__":
    # Get the inputs
    auto, api_whisper, api_gpt  =  get_inputs()

    # Get the model
    whs_model = get_whisper_model(api_whisper)

    # Run the main function
    main(whs_model, auto)





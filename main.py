
import argparse
from whs import load_model
from overlay import launch_overlay


def get_inputs():
    parser = argparse.ArgumentParser(description='Toggle between Local LLM and ChatGPT.')
    parser.add_argument('--auto', action='store_true', default=False, help='Automatically get commentary')
    parser.add_argument('--local_whisper', action='store_true', default=False, help='Run whisper locally instead of through api')
    
    # Parse the arguments
    args = parser.parse_args()

    # Extract the specific arguments
    auto = args.auto
    local_whisper = args.local_whisper

    return auto, local_whisper

def get_whisper_model(local_whisper):
    if local_whisper:
        whs_model = load_model()
    else:
        whs_model = None
   
    return whs_model

def main(whs_model, use_gpt):

    # Launch the GUI in the main thread
    launch_overlay(whs_model, use_gpt )
    

if __name__ == "__main__":

    auto, local_whisper =  get_inputs()
    whs_model = get_whisper_model(local_whisper)
    main(whs_model, auto)





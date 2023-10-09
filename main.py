
import argparse
from whs import load_model
from overlay import launch_overlay


def get_inputs():
    parser = argparse.ArgumentParser(description='Toggle between Local LLM and ChatGPT.')
    parser.add_argument('--use_gpt4', action='store_true', default=False, help='Will use use ChatGPT with GPT-4 otherwise, by defualt it use a local LLM thorugh the text-generation-webui API')
    parser.add_argument('--use_gpt3', action='store_true', default=False, help='Will use use ChatGPT with GPT-3-Turbo otherwise, by defualt it use a local LLM thorugh the text-generation-webui API')
    args = parser.parse_args()
    use_gpt = False

 
    if args.use_gpt4:
        use_gpt = 'gpt-4'
    if args.use_gpt3:
        use_gpt = 'gpt-3.5-turbo'
    
    return use_gpt

def get_whisper_model():
   
    whs_model = load_model()
   
    return whs_model

def main(whs_model, use_gpt):

    # Launch the GUI in the main thread
    launch_overlay(whs_model, use_gpt )
    

if __name__ == "__main__":

    use_gpt =  get_inputs()
    whs_model = get_whisper_model()
    main(whs_model, use_gpt)






from whs import load_model
from overlay import launch_overlay

def get_whisper_model():
    
    return load_model()

def main(whs_model):

    # Launch the GUI in the main thread
    launch_overlay(whs_model)
    

if __name__ == "__main__":
    whs_model = get_whisper_model()
    main(whs_model)





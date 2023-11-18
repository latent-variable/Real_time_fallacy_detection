import sys
import base64
import threading
from PyQt5.QtCore import Qt, QTimer, QPoint, QByteArray, QBuffer, QIODevice
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QSizeGrip, QPushButton
from PyQt5.QtGui import QPixmap

from openai_wrapper import text_fallacy_classification, openAI_TTS
from real_time_classifier import continuous_audio_transcription
from real_time_classifier import WHISPER_TEXTS
from audio import play_audio, change_playback_speed

GPT_TEXTS = []
class TransparentOverlay(QMainWindow):
    
    def __init__(self, whs_model, auto):
        super().__init__()

        self.whs_model = whs_model
        self.auto = auto
        self.dragPos = QPoint()
        self.opacity = 0.6

        self.initUI()
        

    def initUI(self):
        self.setWindowTitle('Transparent Overlay')
        self.setGeometry(0, 0, 1000, 600)
        self.setWindowOpacity(self.opacity)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Create Scroll Areas
        self.scroll_area1 = QScrollArea(self)
        self.scroll_area2 = QScrollArea(self)

        # Increase the dimensions of the scroll areas
        self.scroll_area1.setMinimumSize(380, 120)
        self.scroll_area2.setMinimumSize(380, 120)
        
        # Create Labels
        self.whisper_label = QLabel('Whisper Output Will Appear Here')
        self.chatgpt_label = QLabel('ChatGPT Output Will Appear Here')

        # Enable word-wrap on labels
        self.whisper_label.setWordWrap(True)
        self.chatgpt_label.setWordWrap(True)

        # Add labels to Scroll Areas
        self.scroll_area1.setWidget(self.whisper_label)
        self.scroll_area2.setWidget(self.chatgpt_label)

        # Enable scroll bars on the scroll areas
        self.scroll_area1.setWidgetResizable(True)
        self.scroll_area2.setWidgetResizable(True)

    
        # Style labels with bold text and increased font size
        self.whisper_label.setStyleSheet('background-color: lightblue; font-weight: bold; font-size: 16px;')
        self.chatgpt_label.setStyleSheet('background-color: lightgreen; font-weight: bold; font-size: 16px;')
       
        # Layout setup
        # QVBoxLayout for the scroll areas
        vbox_layout = QVBoxLayout()
        vbox_layout.addWidget(self.scroll_area2)
        vbox_layout.addWidget(self.scroll_area1)
        
        # QGridLayout to include QVBoxLayout and QSizeGrip
        grid_layout = QGridLayout()
        grid_layout.addLayout(vbox_layout, 0, 0)
        
        # Add QSizeGrip to the QGridLayout
        size_grip = QSizeGrip(self)
        grid_layout.addWidget(size_grip, 1, 1, Qt.AlignBottom | Qt.AlignRight)

        container = QWidget()
        container.setLayout(grid_layout)
        self.setCentralWidget(container)

        # Run the continuous transcription and classification in a separate thread
        self.stop_event = threading.Event()
        self.transcription_thread = threading.Thread(target=continuous_audio_transcription, args=(self.whs_model, self.stop_event))
        self.transcription_thread.start()

        # Timer to update Whisper and ChatGPT outputs
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)

         # Create a label to display the screenshot
        self.screenshot_label = QLabel(self)
        self.screenshot_label.setWordWrap(True)
        vbox_layout.addWidget(self.screenshot_label)

        # Add a button for screen capture
        self.capture_button = QPushButton('Capture Screen', self)
        self.capture_button.clicked.connect(self.start_capture_thread)
        vbox_layout.addWidget(self.capture_button)
    

    def update_labels(self):
        # get_whisper_transcription returns a list of text segments, newest last.
        whisper_segments = get_whisper_transcription()

        # Concatenate the segments and set the label text.
        self.whisper_label.setText("Transcript: " + '- '.join(whisper_segments))

        # Color old response grey new reponse black
        chatgpt_output_list = get_chatgpt_output()
        chatgpt_text = "".join(chatgpt_output_list)
        self.chatgpt_label.setText(f"{chatgpt_text}")

        self.whisper_label.setMouseTracking(True)
        self.chatgpt_label.setMouseTracking(True)
        self.scroll_area1.setMouseTracking(True)
        self.scroll_area2.setMouseTracking(True)
        
    
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()
     

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()


    def keyPressEvent(self, event):
        global TRANSCRIBE
        if event.key() == Qt.Key_Escape:
            # To stop the thread
            self.stop_event.set()
            self.transcription_thread.join()  # Optional: Wait for the thread to finish
            self.close()

    def start_capture_thread(self):
        capture_thread = threading.Thread(target=self.capture_and_process)
        capture_thread.start()

    def capture_and_process(self):
         # Increase transparency to 100%
        self.setWindowOpacity(0.0)

        # Process all pending application events
        QApplication.processEvents()
        
        # Delay the screenshot to ensure the overlay is fully transparent
        self.capture_screen()
        
    def capture_screen(self):
        # Use the overlay's geometry as the capture area
        capture_area = self.geometry()
        # Capture the screen
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow(0, capture_area.x()-50, capture_area.y()-50, capture_area.width()+100, capture_area.height()+100)
        
        # Reset the transparency
        self.setWindowOpacity(self.opacity)  # Assuming 0.6 is your default opacity
        # Process all pending application events
        QApplication.processEvents()

        # Display the screenshot
        self.process_screenshot(screenshot)

    def process_screenshot(self, screenshot):
        # Convert screenshot to QPixmap and display it in the label
        pixmap = QPixmap(screenshot)
        self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(), Qt.KeepAspectRatio))
        print(self.auto)

        # Convert QPixmap to QImage
        image = screenshot.toImage()

        # Scale the image by a factor, e.g., 0.5 for half size
        scale_factor = 0.3
        new_width = image.width() * scale_factor
        new_height = image.height() * scale_factor
        scaled_image = image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        print(scaled_image.width(), scaled_image.height())

        # Prepare a byte array and a buffer to hold the image data
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)

        # Save the image to the buffer in PNG format
        scaled_image.save(buffer, "PNG")

        # Save the image to a file
        file_path = "img/screenshot.png"  # Specify your directory path and file name here
        scaled_image.save(file_path, "PNG")  # Saving as a PNG file

        # Convert byte array to base64
        base64_data = base64.b64encode(byte_array.data()).decode()

        # Format the base64 string for API use
        formatted_base64_image = "data:image/png;base64," + base64_data

        # Here, you can use formatted_base64_image with your API
        # For demonstration, let's just print it
        text = text_fallacy_classification(formatted_base64_image, get_whisper_transcription())

        GPT_TEXTS.append(text)

        # Play GPT4
        # audio_file = openAI_TTS(text)
        # audio_file = change_playback_speed(audio_file)
        # play_audio(audio_file)

        
            

def get_whisper_transcription():
    global WHISPER_TEXTS
    last_n_segments = WHISPER_TEXTS[-9:]  # Assuming you want the last 10 segments
    # text = ' - '.join(last_n_segments)
    return last_n_segments

def get_chatgpt_output():
    global GPT_TEXTS
    if len(GPT_TEXTS):
        return GPT_TEXTS[-1]
    else:
        return [""]

def launch_overlay(whs_model, use_gpt):
    app = QApplication(sys.argv)
    overlay = TransparentOverlay(whs_model, use_gpt)
    overlay.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    launch_overlay()

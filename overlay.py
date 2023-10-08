import sys
import threading
from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QSizeGrip

from real_time_classifier import continuous_audio_transcription_and_classification
from real_time_classifier import WHISPER_TEXTS, GPT_TEXTS, MAX_SEGEMENTS

class TransparentOverlay(QMainWindow):
    def __init__(self, whs_model):
        super().__init__()

        self.whs_model = whs_model
        self.dragPos = QPoint()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Transparent Overlay')
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowOpacity(0.8)
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
        vbox_layout.addWidget(self.scroll_area1)
        vbox_layout.addWidget(self.scroll_area2)
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
        self.transcription_thread = threading.Thread(target=continuous_audio_transcription_and_classification, args=(self.whs_model,self.stop_event))
        self.transcription_thread.start()

        # Timer to update Whisper and ChatGPT outputs
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(500)
    

    def update_labels(self):
        whisper_output = get_whisper_transcription()
        chatgpt_output = get_chatgpt_output()

        self.whisper_label.setText("Transcript: " + whisper_output)
        self.chatgpt_label.setText("LLM: " + chatgpt_output)

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
            

def get_whisper_transcription():
    global WHISPER_TEXTS
    last_n_segments = WHISPER_TEXTS[-12:]
    text = ' - '.join(last_n_segments)
    return text

def get_chatgpt_output():
    global GPT_TEXTS
    # Check if the list has at least two elements
    if len(GPT_TEXTS) >= 2:
        last_two = GPT_TEXTS[-1:-3:-1]  # Get and reverse the last two strings
        text = "\n\n ".join(last_two)  # Combine them
    else:
        text = GPT_TEXTS[-1] if GPT_TEXTS else ""
    
    return text

def launch_overlay(whs_model):
    app = QApplication(sys.argv)
    overlay = TransparentOverlay(whs_model)
    overlay.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    launch_overlay()

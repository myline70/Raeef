import sys
from PyQt6.QtWidgets import QApplication
from ui import MainWindow
from record_question import RecordQuestion
from speech_recognition_helper import SpeechRecognitionHelper

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
import sqlite3
import pyttsx3
from PyQt6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
)
from PyQt6.QtCore import Qt, QTimer
from avatar import AnimatedSvgWidget
from list_window import ListWindow
from add_question_window import AddQuestionWindow
from record_question import RecordQuestion

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("المساعد الشخصي")
        self.setFixedSize(900, 700)

        # تهيئة محرك النصوص إلى كلام
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # سرعة الكلام
        self.engine.setProperty('volume', 1.0)  # مستوى الصوت

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Avatar
        self.avatar = AnimatedSvgWidget()
        layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Label to display text
        self.text_display = QLabel("مرحبًا! كيف يمكنني مساعدتك؟", self)
        self.text_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.text_display)

        # Buttons
        button_layout = QHBoxLayout()
        self.record_btn = QPushButton("تسجيل سؤال")
        self.record_btn.setStyleSheet("background-color: #3AAFA9; color: black;")
        self.record_btn.clicked.connect(self.record_question)
        button_layout.addWidget(self.record_btn)

        add_question_btn = QPushButton("إضافة سؤال")
        add_question_btn.setStyleSheet("background-color: #3AAFA9; color: black;")
        add_question_btn.clicked.connect(self.show_add_question)
        button_layout.addWidget(add_question_btn)

        view_list_btn = QPushButton("قائمة الأسئلة")
        view_list_btn.setStyleSheet("background-color: #3AAFA9; color: black;")
        view_list_btn.clicked.connect(self.show_list_window)
        button_layout.addWidget(view_list_btn)

        close_btn = QPushButton("إغلاق التطبيق")
        close_btn.setStyleSheet("background-color: #FF6B6B; color: black;")
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

        # عرض الترحيب الصوتي بعد ثانية واحدة من التشغيل
        QTimer.singleShot(1000, self.play_intro)

    def play_intro(self):
        self.text_display.setText("مرحبًا! أنا رائف، مساعدك الشخصي.")
        self.engine.say("مرحبًا! أنا رائف، مساعدك الشخصي.")
        self.engine.runAndWait()

    def record_question(self):
        try:
            self.text_display.setText("جاري التسجيل...")
            recorder = RecordQuestion()
            question = recorder.record()
            self.text_display.setText(f"السؤال: {question}")
            self.process_question(question)
        except Exception as e:
            print(f"Error during recording: {e}")
            self.text_display.setText(".")

    def process_question(self, question):
        try:
            conn = sqlite3.connect('questions.db')
            cursor = conn.cursor()
            cursor.execute("SELECT answer FROM qa WHERE question = ?", (question,))
            result = cursor.fetchone()
            conn.close()

            if result:
                answer = result[0]
                self.text_display.setText(f"السؤال: {question}\nالإجابة: {answer}")
                self.speak_answer(answer)
            else:
                self.text_display.setText(f"السؤال: {question}\nعذرًا، لا أملك إجابة لهذا السؤال.")
                self.speak_answer("عذرًا، لا أملك إجابة لهذا السؤال.")
        except Exception as e:
            print(f"Error processing question: {e}")
            self.text_display.setText(".")
            self.speak_answer(".")

    def speak_answer(self, text):
        try:
            self.avatar.start_animation()
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error during speech: {e}")
        finally:
            self.avatar.stop_animation()
            QTimer.singleShot(1000, lambda: self.text_display.setText(""))

    def show_add_question(self):
        self.add_question_window = AddQuestionWindow(self)
        self.add_question_window.show()

    def show_list_window(self):
        self.list_window = ListWindow(self)
        self.list_window.show()

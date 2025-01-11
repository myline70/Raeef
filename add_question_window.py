import sqlite3
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QMessageBox
)

class AddQuestionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إضافة سؤال")
        self.setFixedSize(600, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)

        # السؤال
        question_label = QLabel("السؤال:")
        self.question_input = QLineEdit()
        self.question_input.setStyleSheet("background-color: white; color: black;")

        # الإجابة
        answer_label = QLabel("الإجابة:")
        self.answer_input = QTextEdit()
        self.answer_input.setStyleSheet("background-color: white; color: black;")

        # الأزرار
        save_btn = QPushButton("حفظ")
        save_btn.setStyleSheet("background-color: #3AAFA9; color: black;")
        save_btn.clicked.connect(self.save_question)

        close_btn = QPushButton("إغلاق")
        close_btn.setStyleSheet("background-color: #FF6B6B; color: black;")
        close_btn.clicked.connect(self.close)

        # ترتيب العناصر
        layout.addWidget(question_label)
        layout.addWidget(self.question_input)
        layout.addWidget(answer_label)
        layout.addWidget(self.answer_input)

        button_layout = QVBoxLayout()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)

    def save_question(self):
        question = self.question_input.text()
        answer = self.answer_input.toPlainText()

        if question and answer:
            conn = sqlite3.connect('questions.db')
            c = conn.cursor()
            c.execute("INSERT INTO qa (question, answer) VALUES (?, ?)", (question, answer))
            conn.commit()
            conn.close()
            QMessageBox.information(self, "نجاح", "تم حفظ السؤال.")
            self.question_input.clear()
            self.answer_input.clear()
        else:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال السؤال والإجابة.")
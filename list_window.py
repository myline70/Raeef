import sqlite3
import pyttsx3
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QMessageBox, QLineEdit, QTextEdit, QDialog, QLabel
)

class ListWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("قائمة الأسئلة والإجابات")
        self.setFixedSize(800, 500)

        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ت", "السؤال", "الإجابة", "خيارات"])
        layout.addWidget(self.table)
        self.load_data()

        close_btn = QPushButton("إغلاق")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def speak(self, text):
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error in speaking: {e}")

    def load_data(self):
        conn = sqlite3.connect('questions.db')
        c = conn.cursor()
        c.execute("SELECT * FROM qa")
        data = c.fetchall()
        conn.close()

        self.table.setRowCount(len(data))
        for i, row in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[1]))
            self.table.setItem(i, 2, QTableWidgetItem(row[2]))

            button_layout = QHBoxLayout()

            speak_btn = QPushButton("🔊")
            speak_btn.setStyleSheet("color: black; background-color: #CCFFCC;")
            speak_btn.clicked.connect(lambda checked, text=row[2]: self.speak(text))
            button_layout.addWidget(speak_btn)

            delete_btn = QPushButton("حذف")
            delete_btn.setStyleSheet("color: black; background-color: #FFCCCC;")
            delete_btn.clicked.connect(lambda checked, row_id=row[0]: self.delete_row(row_id))
            button_layout.addWidget(delete_btn)

            edit_btn = QPushButton("تعديل")
            edit_btn.setStyleSheet("color: black; background-color: #FFFFCC;")
            edit_btn.clicked.connect(lambda checked, row_data=row: self.edit_row(row_data))
            button_layout.addWidget(edit_btn)

            button_widget = QWidget()
            button_widget.setLayout(button_layout)
            self.table.setCellWidget(i, 3, button_widget)

    def delete_row(self, row_id):
        reply = QMessageBox.question(self, "تأكيد", "هل تريد حذف هذا السؤال؟",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('questions.db')
            c = conn.cursor()
            c.execute("DELETE FROM qa WHERE id=?", (row_id,))
            conn.commit()
            conn.close()
            self.load_data()
            self.speak("تم حذف السؤال.")

    def edit_row(self, row_data):
        dialog = QDialog(self)
        dialog.setWindowTitle("تعديل السؤال")
        dialog.setFixedSize(400, 300)

        layout = QVBoxLayout(dialog)
        question_input = QLineEdit(dialog)
        question_input.setText(row_data[1])
        question_input.setStyleSheet("background-color: white; color: black;")
        answer_input = QTextEdit(dialog)
        answer_input.setText(row_data[2])
        answer_input.setStyleSheet("background-color: white; color: black;")
        save_btn = QPushButton("حفظ", dialog)
        save_btn.clicked.connect(lambda: self.save_edit(row_data[0], question_input.text(), answer_input.toPlainText(), dialog))
        close_btn = QPushButton("إغلاق", dialog)
        close_btn.clicked.connect(dialog.close)

        layout.addWidget(QLabel("السؤال:", dialog))
        layout.addWidget(question_input)
        layout.addWidget(QLabel("الإجابة:", dialog))
        layout.addWidget(answer_input)
        layout.addWidget(save_btn)
        layout.addWidget(close_btn)

        dialog.exec()

    def save_edit(self, question_id, question, answer, dialog):
        if question and answer:
            conn = sqlite3.connect('questions.db')
            c = conn.cursor()
            c.execute("UPDATE qa SET question=?, answer=? WHERE id=?", (question, answer, question_id))
            conn.commit()
            conn.close()
            self.load_data()
            dialog.close()
            QMessageBox.information(self, "نجاح", "تم تعديل السؤال.")
            self.speak("تم تعديل السؤال بنجاح.")
        else:
            QMessageBox.warning(self, "خطأ", "يرجى إدخال السؤال والإجابة.")
            self.speak("يرجى إدخال السؤال والإجابة.")

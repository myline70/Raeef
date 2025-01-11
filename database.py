
import sqlite3

class Database:
    def __init__(self, db_file="questions.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS qa_pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_qa_pair(self, question, answer):
        self.cursor.execute('INSERT INTO qa_pairs (question, answer) VALUES (?, ?)', (question, answer))
        self.conn.commit()

    def get_all_qa_pairs(self):
        self.cursor.execute('SELECT * FROM qa_pairs')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

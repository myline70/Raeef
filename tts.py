import pyttsx3

class TextToSpeech:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # سرعة الكلام
        self.engine.setProperty('volume', 1.0)  # مستوى الصوت

    def speak(self, text):
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in Text-to-Speech: {e}")
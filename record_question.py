import speech_recognition as sr

class RecordQuestion:
    def __init__(self, process_question_callback=None):
        """
        process_question_callback: دالة لمعالجة السؤال المسجل.
        """
        self.recognizer = sr.Recognizer()
        self.process_question_callback = process_question_callback

    def record(self):
        try:
            print("Initializing microphone...")
            with sr.Microphone() as source:
                print("Microphone initialized successfully.")
                print("Listening for the question...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
                print("Processing the audio...")
                # استخدام واجهة Google للتعرف على النص
                question = self.recognizer.recognize_google(audio, language='ar-AR')
                print(f"Recognized Question: {question}")

                # إذا كان هناك دالة لمعالجة السؤال، يتم استدعاؤها
                if self.process_question_callback:
                    self.process_question_callback(question)

                return question
        except sr.UnknownValueError:
            print("Could not understand the question.")
            return "لم أتمكن من فهم السؤال."
        except sr.RequestError as e:
            print(f"API request error: {e}")
            return f"حدث خطأ أثناء الاتصال بالخدمة: {e}"
        except Exception as e:
            print(f"Unexpected error: {e}")
            return f"خطأ غير متوقع: {e}"
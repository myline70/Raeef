import speech_recognition as sr

class SpeechRecognitionHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def listen(self):
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source)

            return self.recognizer.recognize_google(audio, language="ar-AR")
        except sr.UnknownValueError:
            return "لم أتمكن من فهم السؤال."
        except sr.RequestError:
            return "خطأ في الاتصال بالخدمة."
        except Exception as e:
            print(f"Error in Speech Recognition: {e}")
            return "حدث خطأ غير متوقع."
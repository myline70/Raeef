import speech_recognition as sr

class SpeechRecognitionHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_microphone_index(self):
        try:
            mic_names = sr.Microphone.list_microphone_names()
            if not mic_names:
                print("❌ لا توجد أجهزة مايكروفون متاحة.")
                return None

            print("🎙️ المايكروفونات المتاحة:")
            for i, name in enumerate(mic_names):
                print(f"[{i}] {name}")

            return 0  # نختار أول جهاز متاح
        except Exception as e:
            print(f"⚠️ خطأ أثناء فحص المايكروفونات: {e}")
            return None

    def listen(self):
        try:
            mic_index = self.get_microphone_index()
            if mic_index is None:
                return "لم يتم العثور على مايكروفون."

            with sr.Microphone(device_index=mic_index) as source:
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

import speech_recognition as sr

class SpeechRecognitionHelper:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def get_available_microphone_index(self):
        try:
            mic_names = sr.Microphone.list_microphone_names()
            for index, name in enumerate(mic_names):
                try:
                    # نحاول نفتح المايكروفون للتأكد أنه شغال
                    with sr.Microphone(device_index=index) as source:
                        return index  # أول مايكروفون شغال نستخدمه
                except:
                    continue
            return None
        except Exception as e:
            print(f"⚠️ خطأ أثناء فحص المايكروفونات: {e}")
            return None

    def listen(self):
        try:
            mic_index = self.get_available_microphone_index()
            if mic_index is None:
                return "❌ لم يتم العثور على مايكروفون شغال."

            with sr.Microphone(device_index=mic_index) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("🎤 استمع الآن...")
                audio = self.recognizer.listen(source)

            return self.recognizer.recognize_google(audio, language="ar-AR")

        except sr.UnknownValueError:
            return "❗ لم أتمكن من فهم الصوت."
        except sr.RequestError:
            return "🚫 خطأ في الاتصال بخدمة جوجل."
        except Exception as e:
            print(f"⚠️ حدث خطأ في التعرف على الصوت: {e}")
            return "حدث خطأ غير متوقع أثناء الاستماع."

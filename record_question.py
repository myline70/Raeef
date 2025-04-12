import speech_recognition as sr

class RecordQuestion:
    def __init__(self, process_question_callback=None):
        """
        process_question_callback: دالة تُستدعى بعد التعرف على السؤال.
        """
        self.recognizer = sr.Recognizer()
        self.process_question_callback = process_question_callback

    def get_microphone_index(self):
        try:
            mic_names = sr.Microphone.list_microphone_names()
            if not mic_names:
                print("❌ لا توجد أجهزة مايكروفون متاحة.")
                return None

            print("🎙️ الأجهزة المتاحة:")
            for i, name in enumerate(mic_names):
                print(f"[{i}] {name}")

            return 0  # نختار أول جهاز تلقائياً
        except Exception as e:
            print(f"⚠️ خطأ أثناء فحص المايكروفونات: {e}")
            return None

    def record(self):
        try:
            print("🔄 جاري تهيئة المايكروفون...")
            mic_index = self.get_microphone_index()
            if mic_index is None:
                return "لم يتم العثور على مايكروفون."

            with sr.Microphone(device_index=mic_index) as source:
                print("🎤 جاهز للاستماع...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

            print("⏳ جاري تحويل الصوت إلى نص...")
            question = self.recognizer.recognize_google(audio, language='ar-AR')
            print(f"✅ النص المُتعرّف عليه: {question}")

            if self.process_question_callback:
                self.process_question_callback(question)

            return question

        except sr.UnknownValueError:
            print("❗ لم يتم فهم السؤال.")
            return "لم أتمكن من فهم السؤال."
        except sr.RequestError as e:
            print(f"❗ مشكلة في الاتصال: {e}")
            return f"حدث خطأ أثناء الاتصال بالخدمة: {e}"
        except Exception as e:
            print(f"❗ خطأ غير متوقع: {e}")
            return f"خطأ غير متوقع: {e}"

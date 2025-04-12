import speech_recognition as sr

class RecordQuestion:
    def __init__(self, process_question_callback=None):
        """
        process_question_callback: دالة لمعالجة السؤال المسجل.
        """
        self.recognizer = sr.Recognizer()
        self.process_question_callback = process_question_callback

    def get_microphone_index(self):
        try:
            mic_names = sr.Microphone.list_microphone_names()
            if not mic_names:
                print("❌ لا توجد أجهزة مايكروفون متاحة.")
                return None

            print("🎙️ المايكروفونات المتاحة:")
            for i, name in enumerate(mic_names):
                print(f"[{i}] {name}")

            # نختار أول مايكروفون متاح
            return 0
        except Exception as e:
            print(f"⚠️ خطأ أثناء فحص المايكروفونات: {e}")
            return None

    def record(self):
        try:
            print("🎤 بدء تشغيل المايكروفون...")
            mic_index = self.get_microphone_index()
            if mic_index is None:
                return "❌ لم يتم العثور على مايكروفون."

            with sr.Microphone(device_index=mic_index) as source:
                print("🎧 جاري الاستماع...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

            print("🔍 جاري التعرف على الكلام...")
            question = self.recognizer.recognize_google(audio, language='ar-AR')
            print(f"✅ تم التعرف على السؤال: {question}")

            if self.process_question_callback:
                self.process_question_callback(question)

            return question.strip()

        except sr.UnknownValueError:
            print("❗ لم يتم فهم السؤال.")
            return ""
        except sr.RequestError as e:
            print(f"🌐 مشكلة في الاتصال بالخدمة: {e}")
            return "خطأ في الاتصال بالخدمة."
        except Exception as e:
            print(f"❗ خطأ غير متوقع: {e}")
            return "حدث خطأ غير متوقع."

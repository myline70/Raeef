import speech_recognition as sr
import pyaudio  # مهم جدًا لضمان عمل المايك على ويندوز

class RecordQuestion:
    def __init__(self, process_question_callback=None):
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

            return 0  # اختر أول مايكروفون تلقائيًا
        except Exception as e:
            print(f"⚠️ خطأ أثناء فحص المايكروفونات: {e}")
            return None

    def record(self):
        try:
            print("🟡 تهيئة المايكروفون...")
            mic_index = self.get_microphone_index()
            if mic_index is None:
                return "❌ لم يتم العثور على مايكروفون."

            with sr.Microphone(device_index=mic_index) as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("🎤 استمع الآن...")
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)

            print("✅ تم التسجيل، جارٍ التحويل لنص...")
            question = self.recognizer.recognize_google(audio, language='ar-AR')
            print(f"📥 السؤال: {question}")

            if self.process_question_callback:
                self.process_question_callback(question)

            return question

        except sr.UnknownValueError:
            return "لم أتمكن من فهم السؤال."
        except sr.RequestError as e:
            return f"خطأ في الاتصال بالخدمة: {e}"
        except Exception as e:
            print(f"❌ خطأ غير متوقع: {e}")
            return f"حدث خطأ غير متوقع: {e}"

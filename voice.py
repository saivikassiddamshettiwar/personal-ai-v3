import speech_recognition as sr
import pyttsx3

_engine = pyttsx3.init()


def listen_to_voice():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

        text = recognizer.recognize_google(audio)
        return text

    except sr.WaitTimeoutError:
        return ""
    except sr.UnknownValueError:
        return ""
    except Exception as e:
        print(f"Voice input error: {e}")
        return ""


def speak_text(text):
    try:
        _engine.say(text)
        _engine.runAndWait()
    except Exception as e:
        print(f"Voice output error: {e}")

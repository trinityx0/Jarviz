import speech_recognition as sr
import sounddevice as sd

print("JARVIZ: Microphone test starting...")

def listen():
    recognizer = sr.Recognizer()

    try:
        print("JARVIZ: Listening... Speak now!")

        sample_rate = 16000
        duration = 5

        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        print("JARVIZ: Processing your voice...")

        audio = sr.AudioData(
            recording.tobytes(),
            sample_rate,
            2
        )

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You said:", command)
        return command

    except sr.UnknownValueError:
        print("JARVIZ: Sorry, I couldn't understand.")

    except sr.RequestError:
        print("JARVIZ: Speech recognition service unavailable.")

    except Exception as error:
        print("Microphone error:", error)

    return None


listen()
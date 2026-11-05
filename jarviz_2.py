import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser


# ==========================================
# JARVIZ V2.3
# ==========================================

ASSISTANT_NAME = "JARVIZ"
SAMPLE_RATE = 16000
RECORD_SECONDS = 5

recognizer = sr.Recognizer()
engine = None


# ==========================================
# VOICE ENGINE
# ==========================================

def initialize_voice():

    global engine

    engine = pyttsx3.init('sapi5')

    engine.setProperty('rate', 175)
    engine.setProperty('volume', 1.0)

    print("Voice system initialized.")


def speak(message):

    print(f"\n{ASSISTANT_NAME}: {message}")

    try:

        engine.say(message)
        engine.runAndWait()

    except Exception as error:

        print("VOICE ERROR:", error)


# ==========================================
# LISTENING SYSTEM
# ==========================================

def listen():

    print("\nListening...")

    try:

        audio_data = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype='int16'
        )

        sd.wait()

        audio = sr.AudioData(
            audio_data.tobytes(),
            SAMPLE_RATE,
            2
        )

        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = command.lower().strip()

        print("YOU:", command)

        return command

    except sr.UnknownValueError:

        print("Could not understand.")
        return ""

    except sr.RequestError:

        speak("Speech recognition service unavailable.")
        return ""

    except Exception as error:

        print("MICROPHONE ERROR:", error)
        return ""


# ==========================================
# APPLICATION LAUNCHER
# ==========================================

def open_application(app):

    try:

        if app == "chrome":

            webbrowser.open("https://www.google.com")

        elif app == "notepad":

            subprocess.Popen(["notepad.exe"])

        elif app == "calculator":

            subprocess.Popen(["calc.exe"])

        speak(f"Opening {app}, sir.")

    except Exception as error:

        print("APPLICATION ERROR:", error)

        speak("Unable to open the application.")


# ==========================================
# COMMAND PROCESSING
# ==========================================

def process_command(command):

    command = command.lower().strip()

    if not command:
        return "continue"

    if "open chrome" in command or "open google" in command:

        open_application("chrome")

    elif "open notepad" in command:

        open_application("notepad")

    elif "open calculator" in command:

        open_application("calculator")

    elif "hello" in command or "hey jarviz" in command:

        speak("Hello sir. How can I help you?")

    elif "how are you" in command:

        speak("All systems operational, sir.")

    elif "exit" in command or "stop assistant" in command:

        speak("Shutting down. Goodbye, sir.")

        return "exit"

    else:

        speak("I am still learning that command, sir.")

    return "continue"


# ==========================================
# MAIN SYSTEM
# ==========================================

def main():

    try:

        initialize_voice()

        speak("JARVIZ is online. How can I help you?")

        while True:

            command = listen()

            result = process_command(command)

            if result == "exit":

                break

    except KeyboardInterrupt:

        print("\nJARVIZ stopped.")

    except Exception as error:

        print("SYSTEM ERROR:", error)

    finally:

        if engine:

            engine.stop()


# ==========================================
# START JARVIZ
# ==========================================

if __name__ == "__main__":

    main()
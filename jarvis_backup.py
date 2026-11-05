import datetime
import random
import time
import subprocess

import numpy as np
import sounddevice as sd
import speech_recognition as sr


# ==================================================
# JARVIZ - PERSONAL VOICE ASSISTANT
# ==================================================

ASSISTANT_NAME = "JARVIZ"

SAMPLE_RATE = 16000
RECORD_SECONDS = 5
LANGUAGE = "en-IN"

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True


# ==================================================
# WINDOWS NATIVE VOICE ENGINE
# ==================================================

def initialize_voice():

    print("Initializing JARVIZ voice system...")

    success = speak("JARVIZ voice system online.")

    if success:
        print("Windows speech engine initialized successfully.")
    else:
        print("WARNING: Voice initialization failed.")

    return success


def speak(message):

    message = str(message)

    print(f"\n{ASSISTANT_NAME}: {message}")

    # Windows native speech engine
    powershell_script = r"""
Add-Type -AssemblyName System.Speech

$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer

$speaker.Volume = 100
$speaker.Rate = 0

$text = [Console]::In.ReadToEnd()

if (-not [string]::IsNullOrWhiteSpace($text)) {
    $speaker.Speak($text)
}

$speaker.Dispose()
"""

    try:

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                powershell_script
            ],

            input=message,

            text=True,

            encoding="utf-8",

            capture_output=True,

            timeout=60,

            check=True,

            creationflags=getattr(
                subprocess,
                "CREATE_NO_WINDOW",
                0
            )
        )

        print("[JARVIZ VOICE] Response spoken successfully.")

        return True

    except subprocess.TimeoutExpired:

        print("[VOICE ERROR] Speech timed out.")

        return False

    except subprocess.CalledProcessError as error:

        print("[VOICE ERROR]", error.stderr)

        return False

    except Exception as error:

        print("[VOICE ERROR]", error)

        return False


# ==================================================
# MICROPHONE AND SPEECH RECOGNITION
# ==================================================

def listen():

    try:

        print(f"\n{ASSISTANT_NAME}: Listening... Speak now.")

        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        # Check microphone volume

        volume = float(
            np.sqrt(
                np.mean(
                    recording.astype(np.float32) ** 2
                )
            )
        )

        if volume < 30:

            print("JARVIZ: No clear audio detected.")

            return ""

        # Convert recording into speech recognition audio

        audio_data = sr.AudioData(
            recording.tobytes(),
            SAMPLE_RATE,
            2
        )

        print("JARVIZ: Processing your voice...")

        command = recognizer.recognize_google(
            audio_data,
            language=LANGUAGE
        )

        command = command.lower().strip()

        print("YOU SAID:", command)

        return command

    except sr.UnknownValueError:

        print("JARVIZ: I couldn't understand. Try again.")

        return ""

    except sr.RequestError as error:

        print("Recognition service error:", error)

        speak("I cannot reach the speech recognition service.")

        time.sleep(1)

        return ""

    except Exception as error:

        print("MICROPHONE ERROR:", error)

        time.sleep(1)

        return ""


# ==================================================
# DATE AND TIME
# ==================================================

def tell_time():

    current_time = datetime.datetime.now().strftime(
        "%I:%M %p"
    )

    speak(
        f"Sir, the current time is {current_time}."
    )


def tell_date():

    current_date = datetime.datetime.now().strftime(
        "%A, %d %B %Y"
    )

    speak(
        f"Sir, today is {current_date}."
    )


# ==================================================
# MOTIVATIONAL QUOTES
# ==================================================

QUOTES = [

    "Greatness begins where excuses end.",

    "Dream big, work silently, and let success make the noise.",

    "Discipline turns ordinary days into extraordinary results.",

    "Your future is created by what you do today.",

    "Small steps every day lead to remarkable results.",

    "Stay focused on your goals and keep moving forward."

]


def give_quote():

    quote = random.choice(QUOTES)

    speak(f"Here is your quote, sir. {quote}")


# ==================================================
# GREETING
# ==================================================

def greet_user():

    hour = datetime.datetime.now().hour

    if hour < 12:

        greeting = "Good morning"

    elif hour < 17:

        greeting = "Good afternoon"

    else:

        greeting = "Good evening"

    speak(f"{greeting}, sir. JARVIZ is online.")


# ==================================================
# COMMAND PROCESSING
# ==================================================

def process_command(command):

    if not command:

        return True

    command = command.lower().strip()

    # WAKE PHRASES

    wake_phrases = [

        "wake up daddy's home",
        "wake up daddy is home",
        "wake up dad is home",
        "daddy's home",
        "daddy is home",
        "wake up jarviz"

    ]

    if any(phrase in command for phrase in wake_phrases):

        speak("For you always, sir.")

        return True

    # GREETINGS

    if any(phrase in command for phrase in [

        "hello",
        "hi jarviz",
        "hey jarviz"

    ]):

        speak("At your service, sir.")

        return True

    # TIME

    if "time" in command:

        tell_time()

        return True

    # DATE

    if any(word in command for word in [

        "date",
        "today",
        "day is it"

    ]):

        tell_date()

        return True

    # MOTIVATIONAL QUOTES

    if any(word in command for word in [

        "quote",
        "motivation",
        "motivate me"

    ]):

        give_quote()

        return True

    # HELP

    if any(word in command for word in [

        "help",
        "commands",
        "what can you do"

    ]):

        speak(
            "You can ask me for the time, today's date, "
            "a motivational quote, or help. "
            "Say exit to shut me down."
        )

        return True

    # EXIT

    exit_phrases = [

        "exit",
        "quit",
        "shut down",
        "shutdown",
        "go to sleep",
        "goodbye jarviz"

    ]

    if any(phrase in command for phrase in exit_phrases):

        speak(
            "It was a pleasure assisting you, sir. "
            "All systems shutting down. Goodbye."
        )

        return False

    # UNKNOWN COMMAND

    speak(
        "I'm not familiar with that command yet, sir. "
        "Say help to hear the available commands."
    )

    return True


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    print("=" * 50)
    print("       JARVIZ PERSONAL VOICE ASSISTANT")
    print("=" * 50)

    # Initialize voice

    voice_ready = initialize_voice()

    if not voice_ready:

        print("WARNING: Voice output may not work.")

    # Startup announcements

    speak("Initializing all systems.")

    greet_user()

    speak(
        "Voice recognition is ready. "
        "Ask me for the time, date, a quote, or help. "
        "Say exit when you wish to shut me down."
    )

    # Main listening loop

    running = True

    while running:

        command = listen()

        if command:

            running = process_command(command)

    print("\nJARVIZ has shut down.")


# ==================================================
# START JARVIZ
# ==================================================

if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print("\nManual shutdown initiated.")

        speak("Manual shutdown initiated. Goodbye, sir.")

    except Exception as error:

        print("\nUNEXPECTED PROGRAM ERROR:", error)
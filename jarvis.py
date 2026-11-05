import datetime
import random
import time
import subprocess
import re

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

def speak(message):

    message = str(message)

    print(f"\n{ASSISTANT_NAME}: {message}")

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

        subprocess.run(
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


def initialize_voice():

    print("Initializing JARVIZ voice system...")

    success = speak("JARVIZ voice system online.")

    if success:
        print("Windows speech engine initialized successfully.")
    else:
        print("WARNING: Voice initialization failed.")

    return success


# ==================================================
# MICROPHONE AND SPEECH RECOGNITION
# ==================================================

def listen():

    try:

        print(f"\n{ASSISTANT_NAME}: Listening...")

        recording = sd.rec(
            int(RECORD_SECONDS * SAMPLE_RATE),
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        volume = float(
            np.sqrt(
                np.mean(
                    recording.astype(np.float32) ** 2
                )
            )
        )

        if volume < 30:

            print("No clear audio detected.")
            return ""

        audio_data = sr.AudioData(
            recording.tobytes(),
            SAMPLE_RATE,
            2
        )

        print("Processing your voice...")

        command = recognizer.recognize_google(
            audio_data,
            language=LANGUAGE
        )

        command = command.lower().strip()

        print("YOU SAID:", command)

        return command

    except sr.UnknownValueError:

        print("JARVIZ: I couldn't understand.")
        return ""

    except sr.RequestError as error:

        print("Recognition service error:", error)
        return ""

    except Exception as error:

        print("MICROPHONE ERROR:", error)
        time.sleep(1)
        return ""


# ==================================================
# COMMAND NORMALIZATION
# ==================================================

def normalize(command):

    command = command.lower().strip()
    command = command.replace("’", "'")

    return re.sub(r"\s+", " ", command)


# ==================================================
# WAKE-UP SYSTEM
# ==================================================

WAKE_PHRASES = [

    "wake up daddy's home",
    "wake up daddy is home",
    "wake up dad is home",
    "wake up daddy home",
    "daddy's home",
    "daddy is home",
    "daddy home",
    "wake up jarviz"

]


def is_wake_command(command):

    command = normalize(command)

    return any(
        phrase in command
        for phrase in WAKE_PHRASES
    )


def sleep_mode():

    print("\n" + "=" * 45)
    print("          JARVIZ SLEEP MODE")
    print("=" * 45)

    print("Waiting for wake-up command...")

    while True:

        command = listen()

        if not command:
            continue

        if is_wake_command(command):

            speak("For you always, sir.")

            print("\n[JARVIZ STATUS] AWAKE")

            return


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
# COMMAND PROCESSING
# ==================================================

def process_command(command):

    if not command:
        return "continue"

    command = normalize(command)

    # GO TO SLEEP

    sleep_phrases = [

        "go to sleep",
        "enter sleep mode",
        "sleep now",
        "goodnight jarviz"

    ]

    if any(
        phrase in command
        for phrase in sleep_phrases
    ):

        speak("Going to sleep, sir.")

        return "sleep"

    # GREETINGS

    if any(phrase in command for phrase in [

        "hello",
        "hi jarviz",
        "hey jarviz"

    ]):

        speak("At your service, sir.")

        return "continue"

    # TIME

    if "time" in command:

        tell_time()

        return "continue"

    # DATE

    if any(word in command for word in [

        "date",
        "today",
        "day is it"

    ]):

        tell_date()

        return "continue"

    # MOTIVATIONAL QUOTES

    if any(word in command for word in [

        "quote",
        "motivation",
        "motivate me"

    ]):

        give_quote()

        return "continue"

    # HELP

    if any(word in command for word in [

        "help",
        "commands",
        "what can you do"

    ]):

        speak(
            "You can ask me for the time, today's date, "
            "a motivational quote, or help. "
            "Say go to sleep to enter sleep mode, "
            "or exit to shut me down."
        )

        return "continue"

    # EXIT / SHUTDOWN

    exit_phrases = [

        "exit",
        "quit",
        "shut down",
        "shutdown",
        "goodbye jarviz"

    ]

    if any(
        phrase in command
        for phrase in exit_phrases
    ):

        speak(
            "It was a pleasure assisting you, sir. "
            "All systems shutting down. Goodbye."
        )

        return "exit"

    # UNKNOWN COMMAND

    speak(
        "I'm not familiar with that command yet, sir. "
        "Say help to hear the available commands."
    )

    return "continue"


# ==================================================
# MAIN PROGRAM
# ==================================================

def main():

    print("=" * 50)
    print("       JARVIZ PERSONAL VOICE ASSISTANT")
    print("=" * 50)

    initialize_voice()

    speak(
        "All systems initialized. "
        "Entering sleep mode."
    )

    # START IN SLEEP MODE

    running = True

    while running:

        # SLEEP UNTIL WAKE PHRASE

        sleep_mode()

        # AWAKE COMMAND LOOP

        while True:

            command = listen()

            if not command:
                continue

            result = process_command(command)

            if result == "sleep":

                # Return to sleep mode
                break

            elif result == "exit":

                # Shut down completely
                running = False
                break

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

        speak("An unexpected system error occurred.")
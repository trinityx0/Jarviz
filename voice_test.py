import win32com.client
from datetime import datetime

# ==========================================
# JARVIZ - PERSONAL VOICE ASSISTANT
# Windows SAPI speech engine
# ==========================================

speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Configure speech volume and speed
speaker.Volume = 100
speaker.Rate = 0

# Select Microsoft David if available
for voice in speaker.GetVoices():
    if "david" in voice.GetDescription().lower():
        speaker.Voice = voice
        break


# ==========================================
# SPEAK FUNCTION
# Every message is spoken synchronously
# ==========================================

def speak(message):
    print("JARVIZ:", message, flush=True)

    # 0 means speak synchronously:
    # wait until this message finishes
    speaker.Speak(message, 0)


# ==========================================
# STARTUP INTRODUCTION
# ==========================================

def startup():
    messages = [
        "Hello, Abdullah  .",
        "I am Jarviz, your personal assistant.",
        "Initializing all systems.",
        "Voice module is online.",
        "Command interface is ready.",
        "All systems are operational.",
        "I will be your AI assistant.",
        "How may I help you today?"
    ]

    for message in messages:
        speak(message)


# ==========================================
# COMMAND SYSTEM
# ==========================================

def handle_command(command):

    if command in ["hello", "hi", "hey"]:
        speak("Hello,  Abdullah. How can I help you?")

    elif command == "time":
        current_time = datetime.now().strftime("%I:%M %p")
        speak(f" Abdullah the current time is {current_time}.")

    elif command == "date":
        current_date = datetime.now().strftime("%d %B %Y")
        speak(f" Abdullah today's date is {current_date}.")

    elif command in [
        "quote",
        "give me a quote",
        "motivation",
        "motivational quote"
    ]:
        speak("Here is your quote Abdullah")  
        speak("Editing is the transformation of chance into destiny.")

    elif command == "help":
        speak(
            "My available commands are hello, time, date, "
            "give me a quote, help, and exit."
        )

    elif command in ["exit", "quit", "shutdown"]:
        speak("It was a pleasure assisting you, Abdullah.")
        speak("All systems shutting down. Goodbye.")
        return False

    else:
        speak(
            "Sorry, I do not recognize that command yet,. "
            "Type help to hear my available commands."
        )

    return True


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():
    try:
        startup()

        speak("JARVIZ is ready for your commands Abdullah")

        while True:
            command = input("\nYou: ").strip().lower()

            if not command:
                continue

            if not handle_command(command):
                break

    except KeyboardInterrupt:
        print("\nJARVIZ stopped.")

    except Exception as error:
        print("JARVIZ error:", error)

    finally:
        print("JARVIZ session ended.")


if __name__ == "__main__":
    main()
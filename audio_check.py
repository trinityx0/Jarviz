import pyttsx3

print("Initializing Jarviz voice...")

engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")
print("Available voices:", len(voices))

for i, voice in enumerate(voices):
    print(i, voice.name)

if voices:
    engine.setProperty("voice", voices[0].id)

print("Speaking test...")
engine.say("Hello sir. Jarviz voice system is working.")
engine.runAndWait()

print("Voice test finished.")
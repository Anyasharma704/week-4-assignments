import datetime as dt
import platform
import subprocess
import webbrowser
from urllib.parse import quote

import pyttsx3
import speech_recognition as sr

speaker = pyttsx3.init()
speaker.setProperty("rate", 175)


def speak(message):
    print("Assistant:", message)
    speaker.say(message)
    speaker.runAndWait()


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You:", command)
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable. Check your internet.")
    except sr.WaitTimeoutError:
        speak("I didn't hear anything.")
    return ""


def handle_command(command):
    if not command:
        return True

    if "time" in command:
        now = dt.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}.")

    elif "date" in command:
        today = dt.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {today}.")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif command.startswith("search for "):
        query = command.replace("search for ", "", 1).strip()
        webbrowser.open("https://www.google.com/search?q=" + quote(query))
        speak(f"Searching Google for {query}.")

    elif command.startswith("play "):
        query = command.replace("play ", "", 1).strip()
        webbrowser.open("https://www.youtube.com/results?search_query=" + quote(query))
        speak(f"Showing YouTube results for {query}. Choose what you want to play.")

    elif "open calculator" in command and platform.system() == "Windows":
        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator.")

    elif "open notepad" in command and platform.system() == "Windows":
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad.")

    elif "stop" in command or "exit" in command or "goodbye" in command:
        speak("Goodbye!")
        return False

    else:
        speak("I don't have that action yet. Try asking for the time, date, Google, YouTube, or a search.")

    return True


def main():
    speak("Hello! I am your voice assistant.")
    speak("Say a command, or say stop to exit.")
    running = True

    while running:
        try:
            command = listen()
            running = handle_command(command)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except OSError as error:
            speak("I could not access the microphone.")
            print("Microphone error:", error)
            break


if __name__ == "__main__":
    main()

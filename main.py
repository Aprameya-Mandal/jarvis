import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import sys
import random
from playsound import playsound  # pip install playsound

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Jarvis Sir. Please tell me how may I help you")


def recognize_speech_from_mic(recognizer, microphone):
    print("Listening...")
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response


def execommand(query):
    # Logic for executing tasks based on query
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        speak("Opening")
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        speak("Opening")
        webbrowser.open("google.com")

    elif 'open stackoverflow' in query:
        speak("Opening")
        webbrowser.open("stackoverflow.com")

    elif 'play music' in query:
        music_dir = 'C:\\Users\\Mita\\Desktop\\FileBrowser\\Music'
        songs = os.listdir(music_dir)
        random_music = songs[random.randint(0, 11)]
        speak("Playing" + random_music)
        playsound(music_dir + '\\' + random_music)

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Sir, the time is {strTime}")

    elif 'open code' in query:
        codePath = "C:\\Users\\Mita\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'open pycharm' in query:
        pycharmPath = "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.2.2\\bin\\pycharm64.exe"
        os.startfile(pycharmPath)

    elif 'open idol' in query:
        idlePath = "C:\\Users\\Mita\\AppData\\Local\\Programs\\Python\\Python39\\Lib\\idlelib\\idle.pyw"
        os.startfile(idlePath)

    elif "pause" in query:
        input("To start you can press enter...")

    elif 'quit' or 'exit' == query:
        sys.exit()


if __name__ == "__main__":
    speak("Hello sir")
    wishMe()
    while True:
        query = recognize_speech_from_mic(sr.Recognizer(), sr.Microphone())["transcription"]
        if query is not None:
            query = query.lower()
            print("User said: ", query)
            execommand(query)
        else:
            print("So sorry.. Didn't catch that.")
            print("Say that again please...")

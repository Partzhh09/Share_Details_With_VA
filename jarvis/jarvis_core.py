import matplotlib
matplotlib.use("TkAgg")

import speech_recognition as sr
import pyttsx3
import requests
import matplotlib.pyplot as plt

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable")
        return ""


def show_price_chart(symbol, name):
    url = f"http://127.0.0.1:8000/ipo/chart/{symbol}"
    r = requests.get(url)
    result = r.json()

    if "data" not in result:
        speak("Chart data not available")
        return

    times = [p["time"] for p in result["data"]]
    prices = [p["price"] for p in result["data"]]

    plt.figure()
    plt.plot(times, prices)
    plt.title(f"{name} - Last 1 Day Price")
    plt.xlabel("Time")
    plt.ylabel("Price (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    speak(f"Showing price chart for {name}")
    plt.show()


def start_jarvis():
    speak("Jarvis online. Backend initialized.")

    while True:
        command = listen()

        if "price chart" in command:
            show_price_chart("TCS.NS", "TCS")

        elif command.strip() == "exit":
            speak("Shutting down")
            break

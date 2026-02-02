import speech_recognition as sr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import pyttsx3
import requests
import matplotlib
matplotlib.use("TkAgg")

# Initialize voice
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

    # ---- Convert time strings to datetime ----
    times = [
        datetime.strptime(t["time"], "%H:%M")
        for t in result["data"]
    ]
    prices = [p["price"] for p in result["data"]]

    # ---- PLOT ----
    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, linewidth=2)

    plt.title(f"{name} - Last 1 Day Price")
    plt.xlabel("Time")
    plt.ylabel("Price (INR)")

    # ---- FIX X AXIS ----
    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # every 30 min
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()

    speak(f"Showing price chart for {name}")
    plt.show()

def extract_stock_name(command):
    words = command.split()

    if "of" in words:
        idx = words.index("of")
        if idx + 1 < len(words):  # SAFE CHECK
            return words[idx + 1].upper()

    return None

def extract_ipo_name(command):
    words = command.split()
    if "predict" in words:
        index = words.index("predict")
        if index + 1 < len(words):
            return words[index + 1]
    return None

def get_live_price(symbol):
    url = f"http://127.0.0.1:8000/ipo/price/{symbol}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    return None

def predict_ipo(ipo_name):
    url = f"http://127.0.0.1:8000/ipo/predict/{ipo_name}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        print("\n================ IPO DETAILS ================")
        print(f"IPO Name           : {data['ipo']}")
        print(f"Company            : {data['company']}")
        print(f"Issue Price        : {data['issue_price']}")
        print(f"Expected Listing   : {data['listing_price_expected']}")
        print(f"Prediction         : {data['prediction']}")
        print(f"Expected Gain      : {data['expected_gain']}")
        print(f"Risk Level         : {data['risk_level']}")
        print(f"Recommendation     : {data['recommendation']}")
        print("============================================\n")

        return (
            f"{data['ipo']} IPO shows a {data['prediction']} outlook. "
            f"Expected gain is {data['expected_gain']}. "
            f"Risk level is {data['risk_level']}."
        )
    else:
        return "Sorry, I could not fetch IPO data."

def fetch_live_ipos():
    url = "http://127.0.0.1:8000/ipo/live"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def display_live_ipos(ipos):
    if ipos:
        print("\n================ LIVE IPOs ================")
        for ipo in ipos:
            print(f"Name: {ipo['name']}")
            print(f"Status: {ipo['status']}")
            print(f"Expected Listing: {ipo['expected_listing']}")
            print(f"Expected Gain: {ipo['expected_gain']}")
            print(f"Risk Level: {ipo['risk_level']}")
        print("============================================\n")
    else:
        print("No live IPOs found.")

speak("Jarvis online. You can ask for share price or price chart.")

while True:
    command = listen()

    if not command:
        continue  # ignore silence

    elif "price chart" in command or "chart" in command:
        name = extract_stock_name(command)

        if not name:
            speak("Please say the stock name. For example, say price chart of T C S.")
            continue

        symbol = f"{name}.NS"
        speak(f"Showing price chart of {name}")
        show_price_chart(symbol, name)

    elif "price" in command:
        words = command.split()
        if "of" in words:
            idx = words.index("of")
            if idx + 1 >= len(words):
                speak("Please say the stock name. For example, say price of T C S.")
                continue
            name = words[idx + 1].upper()
            symbol = f"{name}.NS"
            data = get_live_price(symbol)

            if data and "price" in data:
                print("\n====== LIVE SHARE PRICE ======")
                print(f"Stock    : {data['symbol']}")
                print(f"Price    : ₹{data['price']}")
                print(f"Exchange : {data['exchange']}")
                print(f"Time     : {data['time']}")
                print("==============================\n")
                speak(f"{name} is trading at rupees {data['price']}")
            else:
                speak("Unable to fetch share price")

    elif command.strip() == "exit":
        speak("Shutting down. Goodbye.")
        break
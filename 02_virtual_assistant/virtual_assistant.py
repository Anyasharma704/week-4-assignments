import datetime as dt
import os
import platform
import subprocess
import threading
import time
import webbrowser
from pathlib import Path
from urllib.parse import quote

import feedparser
import requests

HEADERS = {"User-Agent": "StudentVirtualAssistant/1.0 (educational project)"}


def get_weather():
    city = input("Enter city: ").strip()
    if not city:
        return

    try:
        geo_url = "https://geocoding-api.open-meteo.com/v1/search"
        geo = requests.get(
            geo_url, params={"name": city, "count": 1, "language": "en"},
            headers=HEADERS, timeout=15
        )
        geo.raise_for_status()
        results = geo.json().get("results", [])
        if not results:
            print("City not found.")
            return

        place = results[0]
        forecast_url = "https://api.open-meteo.com/v1/forecast"
        response = requests.get(
            forecast_url,
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m",
            },
            headers=HEADERS, timeout=15
        )
        response.raise_for_status()
        current = response.json()["current"]
        print(f"\nWeather in {place['name']}, {place.get('country', '')}")
        print(f"Temperature: {current['temperature_2m']} °C")
        print(f"Feels like: {current['apparent_temperature']} °C")
        print(f"Humidity: {current['relative_humidity_2m']}%")
        print(f"Wind speed: {current['wind_speed_10m']} km/h")
    except requests.RequestException as error:
        print("Weather service error:", error)


def wikipedia_summary():
    topic = input("What topic should I look up? ").strip()
    if not topic:
        return
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(topic.replace(' ', '_'))}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 404:
            print("I couldn't find that Wikipedia page.")
            return
        response.raise_for_status()
        data = response.json()
        print("\n" + data.get("title", topic))
        print(data.get("extract", "No summary available."))
        if data.get("content_urls"):
            print("Read more:", data["content_urls"]["desktop"]["page"])
    except requests.RequestException as error:
        print("Wikipedia service error:", error)


def news_headlines():
    rss_url = "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en"
    try:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            print("No headlines were returned.")
            return
        print("\nTop news headlines:")
        for number, entry in enumerate(feed.entries[:8], start=1):
            print(f"{number}. {entry.title}")
            print(f"   {entry.link}")
    except Exception as error:
        print("Could not fetch news:", error)


def set_reminder():
    message = input("Reminder message: ").strip()
    if not message:
        return
    try:
        seconds = int(input("Remind me in how many seconds? "))
        if seconds <= 0:
            print("Enter a number greater than zero.")
            return
    except ValueError:
        print("Please enter a whole number.")
        return

    def notify():
        time.sleep(seconds)
        print(f"\n\n*** REMINDER: {message} ***\n")

    threading.Thread(target=notify, daemon=True).start()
    print("Reminder set.")


def find_file():
    name = input("Enter exact file name to look for: ").strip()
    if not name:
        return
    matches = []
    # Search only the user's home folder; skip folders that commonly cause
    # permission errors or enormous scans.
    skip = {".git", "node_modules", ".venv", "AppData"}
    home = Path.home()
    for root, dirs, files in os.walk(home):
        dirs[:] = [d for d in dirs if d not in skip]
        if name in files:
            matches.append(Path(root) / name)
            if len(matches) == 10:
                break
    if matches:
        print("Found:")
        for path in matches:
            print(path)
    else:
        print("No matching file found in the home folder.")


def volume_control():
    if platform.system() != "Windows":
        print("Volume control in this starter project is supported on Windows only.")
        return
    print("Use your keyboard's volume keys, or open Windows sound settings.")
    subprocess.Popen(["cmd", "/c", "start", "", "ms-settings:sound"], shell=False)


def main():
    while True:
        print("\n===== VIRTUAL ASSISTANT =====")
        print("1. Current weather")
        print("2. Wikipedia summary")
        print("3. News headlines")
        print("4. Set a reminder")
        print("5. Find a file in your home folder")
        print("6. Open sound settings (Windows)")
        print("7. Open Google")
        print("8. Show current date and time")
        print("9. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            get_weather()
        elif choice == "2":
            wikipedia_summary()
        elif choice == "3":
            news_headlines()
        elif choice == "4":
            set_reminder()
        elif choice == "5":
            find_file()
        elif choice == "6":
            volume_control()
        elif choice == "7":
            webbrowser.open("https://www.google.com")
        elif choice == "8":
            print(dt.datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p"))
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Please choose an option from 1 to 9.")


if __name__ == "__main__":
    main()

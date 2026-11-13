from pathlib import Path
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

DRAFTS_FILE = Path("caption_drafts.txt")


def save_caption():
    caption = input("Write your caption: ").strip()
    if not caption:
        print("Nothing saved: caption was empty.")
        return

    hashtags = input("Enter hashtags (optional, separated by spaces): ").strip()
    draft = caption
    if hashtags:
        draft += "\n\n" + " ".join(
            tag if tag.startswith("#") else f"#{tag}"
            for tag in hashtags.split()
        )

    with DRAFTS_FILE.open("a", encoding="utf-8") as file:
        file.write(draft + "\n" + "-" * 50 + "\n")

    print(f"Caption draft saved in: {DRAFTS_FILE.resolve()}")


def open_instagram():
    options = Options()
    # Selenium Manager (included with modern Selenium) normally manages
    # the compatible ChromeDriver automatically.
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.instagram.com/")
    print("Instagram opened. Sign in manually in the browser.")
    print("Do not enter your password into this Python program.")
    return driver


def open_hashtag(driver):
    tag = input("Enter a hashtag without # (example: photography): ").strip()
    if not tag:
        print("No hashtag entered.")
        return
    driver.get(f"https://www.instagram.com/explore/tags/{quote(tag)}/")
    print("Hashtag page opened. Browse manually in the browser.")


def main():
    driver = None
    while True:
        print("\n--- Instagram Content Assistant ---")
        print("1. Open Instagram in Chrome")
        print("2. Save a caption draft")
        print("3. Open a hashtag page (browser must be open)")
        print("4. Close browser")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            if driver is not None:
                print("Browser is already open.")
            else:
                try:
                    driver = open_instagram()
                except Exception as error:
                    print("Could not start Chrome:", error)
                    print("Check that Chrome is installed and Selenium is updated.")
        elif choice == "2":
            save_caption()
        elif choice == "3":
            if driver is None:
                print("First choose option 1.")
            else:
                try:
                    open_hashtag(driver)
                except Exception as error:
                    print("Could not open hashtag page:", error)
        elif choice == "4":
            if driver is not None:
                driver.quit()
                driver = None
                print("Browser closed.")
            else:
                print("No browser is open.")
        elif choice == "5":
            if driver is not None:
                driver.quit()
            print("Goodbye!")
            break
        else:
            print("Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

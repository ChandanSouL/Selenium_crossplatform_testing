from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from collections import Counter
import re
import os

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")

# Create driver instance
driver = webdriver.Chrome(options=chrome_options)

# Set image directory
image_dir = "article_images"
os.makedirs(image_dir, exist_ok=True)

# Create log file
log_file = "scraper_output.log"


def log_message(message):
    """Write message to console and log file."""
    print(message)
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(message + "\n")


# List to store article titles
titles_list = []


def translate_text(text, target_language='en'):
    """Translate text using RapidAPI Google Translator."""
    url = "https://google-translator9.p.rapidapi.com/v2"

    payload = {
        "q": text,
        "target": target_language,
        "source": "es"  # Assuming the source language is Spanish
    }

    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "0186982fe3msh25bce2938406bbbp1152f2jsn5dd61d61d700",  # Replace with your RapidAPI key
        "X-RapidAPI-Host": "google-translator9.p.rapidapi.com"
    }

    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        translation = response.json()['data']['translations'][0]['translatedText']
        return translation
    except Exception as e:
        log_message(f"Translation failed: {e}")
        return text  # Return original text if translation fails


try:
    # Open El País homepage
    driver.get("https://elpais.com")

    # Handle pop-up for both desktop and mobile
    try:
        accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR,
                 "[id*='notice-agree'], [class*='pmConsentWall-button'], button[aria-label*='Accept and continue']")
            )
        )
        accept_button.click()
        log_message("Pop-up accepted successfully.")
    except (NoSuchElementException, TimeoutException):
        log_message("Accept button not found, continuing...")

    # Navigate to the Opinion section
    opinion_link = driver.find_element(By.LINK_TEXT, "Opinión")
    opinion_link.click()

    # Fetch the first five articles
    articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]

    for idx in range(5):
        try:
            # Re-fetch articles to avoid stale element reference
            articles = driver.find_elements(By.CSS_SELECTOR, "article")[:5]
            article = articles[idx]

            # Get article title and URL
            title_element = article.find_element(By.CSS_SELECTOR, "h2 a")
            title = title_element.text
            article_url = title_element.get_attribute("href")

            # Store the title in the list
            titles_list.append(title)

            log_message(f"\nProcessing Article {idx + 1}: {title}\n{'-' * 40}")

            # Open article page
            driver.get(article_url)

            # Get all headers (if any)
            headers_elements = driver.find_elements(By.CSS_SELECTOR, "h2.a_st")
            headers = [header.text for header in headers_elements]
            headers_text = "\n".join(headers)

            # Get article content using XPath
            paragraphs = driver.find_elements(By.XPATH, "/html/body/article/div[2]//p")
            content = "\n".join([p.text for p in paragraphs])
            if not content:
                content = "Sin Contenido"

            # Log article details
            log_message(f"Title: {title}\n")
            log_message(f"Header: {headers_text}\n")
            log_message(f"Content: {content}\n")

            # Download and save cover image if available
            try:
                img_element = driver.find_element(By.CSS_SELECTOR, "figure img")
                img_url = img_element.get_attribute("src")

                # Download and save cover image
                img_data = requests.get(img_url).content
                img_path = os.path.join(image_dir, f"article_{idx + 1}.jpg")

                with open(img_path, "wb") as img_file:
                    img_file.write(img_data)

                log_message(f"Cover image for article {idx + 1} saved at: {img_path}\n")
            except NoSuchElementException:
                log_message(f"No cover image found for article {idx + 1}.\n")

            # Return to Opinion section
            driver.get("https://elpais.com/opinion/")

        except Exception as e:
            log_message(f"Error processing article {idx + 1}: {e}")

    # Translate titles
    translated_titles = [translate_text(title) for title in titles_list]
    log_message("\nTranslated Titles:")
    for i, translated_title in enumerate(translated_titles):
        log_message(f"Article {i + 1}: {translated_title}")

finally:
    driver.quit()


def find_repeated_words(headers):
    """Identify words repeated more than twice across all headers."""
    # Combine all headers into a single string
    combined_text = " ".join(headers)

    # Use regex to extract words (ignoring case and punctuation)
    words = re.findall(r'\b\w+\b', combined_text.lower())

    # Count the occurrences of each word
    word_counts = Counter(words)

    # Print the word counts for debugging
    log_message("Count word occurrences:")
    for word, count in word_counts.items():
        log_message(f"{word}: {count}")

    # Filter words that are repeated more than twice
    repeated_words = {word: count for word, count in word_counts.items() if count > 2}

    return repeated_words


def print_repeated_words(repeated_words):
    """Print each repeated word along with its count of occurrences."""
    if not repeated_words:
        log_message("No words are repeated more than twice.")
    else:
        log_message("Words repeated more than twice:")
        for word, count in repeated_words.items():
            log_message(f"{word}: {count} occurrences")


# Find and log repeated words
repeated_words = find_repeated_words(translated_titles)
print_repeated_words(repeated_words)

log_message("\nScraping completed. All results saved to scraper_output.log.")

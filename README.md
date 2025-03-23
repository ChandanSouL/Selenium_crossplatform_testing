# Selenium Cross-Platform Testing 🧪🌐

This project automates cross-platform and cross-browser testing using **Selenium**. The script navigates to the Spanish news website **El País**, fetches the top 5 opinion articles, translates their titles into English, downloads associated images, and identifies words repeated more than twice in the article headers.

---

## 📚 **Features**
- Accepts cookie pop-ups dynamically on both desktop and mobile browsers.
- Navigates to the Opinion section of [El País](https://elpais.com/).
- Fetches and processes the first 5 articles.
- Extracts and translates article titles from Spanish to English.
- Downloads and saves cover images for each article.
- Identifies and counts repeated words across translated titles.

---

## 🛠️ **Technologies Used**
- Python 3.x
- Selenium WebDriver
- Chrome/Chromium browser
- Requests Library (for HTTP requests and image downloads)
- Google Translator API (via RapidAPI)

---

## 📥 **Installation**

### 1. Clone the Repository
```bash
git clone https://github.com/ChandanSouL/Selenium_crossplatform_testing.git
cd Selenium_crossplatform_testing
```
### 2. Create and Activate a Virtual Environment
``` bash
# Create a virtual environment
python3 -m venv myenv

# Activate the environment
# For Linux/Mac
source myenv/bin/activate
# For Windows
myenv\Scripts\activate
```
### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
## 🚀 Usage Instructions

### 1, Run the Script
```bash
python main.py
```
### 2. View Logs and Results
The script generates logs and saves article cover images in the article_images directory.

Translated titles and word counts are displayed in the terminal.
## 📂 Project Structure
```bash
.
├── article_images          # Stores downloaded article images
├── main.py                 # Main script to run the automation
├── requirements.txt        # Required Python packages
└── README.md                # Project documentation
```
##  API Configuration
The script uses Google Translator API from RapidAPI.
Replace the API key in the translate_text() function if needed:
```bash
"X-RapidAPI-Key": "YOUR_RAPIDAPI_KEY_HERE"
```



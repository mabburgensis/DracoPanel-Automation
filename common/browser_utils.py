from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import os

def open_browser():
    chrome_options = Options()

    if os.environ.get("GITHUB_ACTIONS") == "true":
        # Sadece CI ortamında headless modda çalış
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        print(">> Github Actions ortamı algılandı: Headless modda başlatılıyor.")
    else:
        print(">> Lokal ortam: GUI açık şekilde başlatılıyor.")

    # --- Tam buraya eklemiş oluyorsun ---
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get("https://operator.dracofusion.com")
    driver.set_window_size(1400, 1000)
    wait = WebDriverWait(driver, 10)
    return driver, wait
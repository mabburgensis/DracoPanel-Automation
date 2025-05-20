import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# === Ekran görüntüsü klasörü ===
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
screenshot_dir = f"screenshots/{timestamp}"
os.makedirs(screenshot_dir, exist_ok=True)

def screenshot(driver, name):
    driver.save_screenshot(f"{screenshot_dir}/{name}.png")

def open_browser():
    chrome_options = Options()

    # Ortam değişkenine göre ayarla (CI/CD mi lokal mi)
    if os.environ.get("GITHUB_ACTIONS") == "true":
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome_user_data")
        print(">> Github Actions ortamı algılandı: Headless + özel user-data-dir ile başlatılıyor.")
    else:
        print(">> Lokal ortam: GUI açık şekilde başlatılıyor.")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    driver.get("https://operator.dracofusion.com")
    driver.set_window_size(1400, 1000)
    wait = WebDriverWait(driver, 10)
    return driver, wait

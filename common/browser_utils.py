import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

# === Ekran görüntüsü klasörü ===
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
screenshot_dir = f"screenshots/{timestamp}"
os.makedirs(screenshot_dir, exist_ok=True)

def screenshot(driver, name):
    driver.save_screenshot(f"{screenshot_dir}/{name}.png")

def open_browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://operator.dracofusion.com")
    driver.set_window_size(1400, 1000)
    wait = WebDriverWait(driver, 10)
    return driver, wait
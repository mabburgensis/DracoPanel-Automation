import time
import random
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementNotInteractableException

from common.browser_utils import open_browser
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.diamonds_locators import DiamondsLocators

def switch_to_game_iframe(driver):
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        src = iframe.get_attribute("src") or ""
        if "diamonds" in src:
            driver.switch_to.frame(iframe)
            return True
    return False

def slow_type(element, value, delay=0.13):
    for ch in value:
        element.send_keys(ch)
        time.sleep(delay)

def login_and_open_diamonds(driver, wait):
    print("🚀 diamonds.py başlatılıyor")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    # Login
    wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
    creds = load_user_data()
    wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT))).send_keys(creds["username"])
    driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
    driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    print("✅ Login başarılı")
    time.sleep(1.2)

    # Diamonds banner
    print("🎮 Diamonds banner’a tıklanıyor...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, DiamondsLocators.DIAMONDS_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    time.sleep(1.2)

    # Real Play
    print("▶️ Real Play’e tıklanıyor...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, DiamondsLocators.REAL_PLAY_BUTTON)))
    real.click()
    time.sleep(3.0)

    print("⌛ Oyun yükleniyor, bahis inputu bekleniyor...")
    for _ in range(20):
        if switch_to_game_iframe(driver):
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, DiamondsLocators.BET_AMOUNT_INPUT)))
                print("✅ Oyun yüklendi!")
                break
            except TimeoutException:
                time.sleep(0.7)
        else:
            time.sleep(0.5)
    # screenshot(driver, "diamonds_game_opened")

def safe_input_and_click(driver, wait, input_xpath, value, button_xpath, retries=3):
    """
    Stale element ve benzeri hatalarda otomatik retry yapar.
    """
    for attempt in range(retries):
        try:
            if not switch_to_game_iframe(driver):
                time.sleep(0.7)
                continue
            bet_input = wait.until(EC.element_to_be_clickable((By.XPATH, input_xpath)))
            bet_input.click()
            time.sleep(0.3)
            bet_input.clear()
            time.sleep(0.15)
            slow_type(bet_input, str(value), delay=0.13)
            time.sleep(0.6)
            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            submit_btn.click()
            return True
        except (StaleElementReferenceException, ElementNotInteractableException, TimeoutException) as e:
            print(f"   🔄 Retry ({attempt+1}) due to: {e}")
            time.sleep(1.2)
    print("   ❌ Bahis input ya da butonuna ulaşılamadı (stabilizasyon hatası)!")
    return False

def play_10_bets(driver, wait):
    print("🎲 10 defa random bahis oynanacak…")
    for bet_num in range(1, 11):
        try:
            amount = random.randint(2, 99)
            print(f"   ➡️ ({bet_num}/10) Bahis miktarı giriliyor: {amount}")
            ok = safe_input_and_click(
                driver, wait,
                DiamondsLocators.BET_AMOUNT_INPUT,
                amount,
                DiamondsLocators.BET_SUBMIT_BUTTON,
                retries=4
            )
            if not ok:
                print("   ⚠️ Bet adımı atlanıyor, bir sonraki tura geçiliyor.")
                continue

            print("   ✅ Bahis gönderildi")
            time.sleep(2.0)

            switch_to_game_iframe(driver)
            try:
                kazanc = wait.until(EC.presence_of_element_located((By.XPATH, DiamondsLocators.WIN_AMOUNT_INPUT)))
                oran = wait.until(EC.presence_of_element_located((By.XPATH, DiamondsLocators.MULTIPLIER_INPUT)))
                print(f"   🔎 Sonuç: Kazanç = {kazanc.get_attribute('value')}, Oran = {oran.get_attribute('value')}")
            except TimeoutException:
                print("   ⚠️ Sonuç alanı bulunamadı!")
            time.sleep(1.7)
        except Exception as e:
            print(f"   ⚠️ Bir hata oluştu (bet {bet_num}): {e}")
            time.sleep(2.0)
    print("\n🎉 Tüm bahisler başarıyla tamamlandı!")

def test_diamonds_flow():
    driver, wait = open_browser()
    login_and_open_diamonds(driver, wait)
    play_10_bets(driver, wait)
    time.sleep(3.0)
    driver.quit()

if __name__ == "__main__":
    test_diamonds_flow()
    sys.exit(0)
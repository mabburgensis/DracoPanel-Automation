import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from common.browser_utils import open_browser
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.dice_locators import DiceLocators

def switch_to_game_iframe(driver):
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        src = iframe.get_attribute("src") or ""
        if "dice" in src:
            driver.switch_to.frame(iframe)
            return True
    return False

def slow_type(element, value, delay=0.13):
    for ch in value:
        element.send_keys(ch)
        time.sleep(delay)

def login_and_open_dice(driver, wait):
    print("🚀 dice.py başlatılıyor")
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

    # Dice banner
    print("🎮 Dice banner’a tıklanıyor...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.DICE_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    time.sleep(1.2)

    # Real Play
    print("▶️ Real Play’e tıklanıyor...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.REAL_PLAY_BUTTON)))
    real.click()

    # --- Real Play sonrası: iframe + bahis input beklemesi ---
    print("⌛ Oyun yükleniyor, bahis inputu bekleniyor...")
    for _ in range(20):
        if switch_to_game_iframe(driver):
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, DiceLocators.BET_AMOUNT_INPUT)))
                print("✅ Oyun yüklendi!")
                break
            except TimeoutException:
                time.sleep(0.7)
        else:
            time.sleep(0.5)
    # screenshot(driver, "dice_game_opened")

def read_results_with_wait(driver, wait, timeout=5):
    # Sonuçlar geç oluşabilir, 5 saniye boyunca aralıklı dene
    start_time = time.time()
    found_buttons = []
    while time.time() - start_time < timeout:
        result_buttons = driver.find_elements(By.XPATH, f"{DiceLocators.RESULT_ROOT_DIV}//button")
        if result_buttons:
            found_buttons = result_buttons
            break
        time.sleep(0.5)
    return found_buttons

def play_10_bets(driver, wait):
    print("🎲 10 defa random bahis oynanacak…")
    for bet_num in range(1, 11):
        try:
            if not switch_to_game_iframe(driver):
                print("   ❌ Oyun iframe bulunamadı!")
                return

            # Bahis miktarı: 1–99 arası TAMSAYI
            amount = random.randint(1, 99)
            amount_str = str(amount)
            print(f"   ➡️ ({bet_num}/10) Bahis miktarı giriliyor: {amount_str}")

            bet_input = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.BET_AMOUNT_INPUT)))
            bet_input.click()
            time.sleep(0.3)
            bet_input.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.15)
            bet_input.send_keys(Keys.DELETE)
            time.sleep(0.3)
            slow_type(bet_input, amount_str, delay=0.13)
            time.sleep(1.1)

            # Kazanma Şansı (1-99 arası random tam sayı)
            chance = random.randint(1, 99)
            chance_str = str(chance)
            print(f"   ➡️ Kazanma Şansı inputu giriliyor: {chance_str}")
            chance_input = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.CHANCE_INPUT)))
            chance_input.click()
            time.sleep(0.3)
            chance_input.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.15)
            chance_input.send_keys(Keys.DELETE)
            time.sleep(0.3)
            slow_type(chance_input, chance_str, delay=0.13)
            time.sleep(1.1)

            submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.BET_SUBMIT_BUTTON)))
            submit_btn.click()
            print("   ✅ Bahis gönderildi")
            time.sleep(2.0)

            switch_to_game_iframe(driver)

            # --- Sabırlı sonuç okuma: tüm geçmişi ve yeni sonucu logla ---
            result_buttons = read_results_with_wait(driver, wait, timeout=5)
            if not result_buttons:
                print("   ⚠️ Sonuç butonu bulunamadı!")
            else:
                kazanc_sayisi = 0
                kayip_sayisi = 0
                for btn in result_buttons:
                    class_attr = btn.get_attribute("class") or ""
                    if "_won_" in class_attr:
                        print(f"   🟢 Kazanç: {btn.text}")
                        kazanc_sayisi += 1
                    elif "_default_" in class_attr:
                        print(f"   🔴 Kayıp: {btn.text}")
                        kayip_sayisi += 1
                if kazanc_sayisi == 0 and kayip_sayisi == 0:
                    print("   ⚠️ Sonuç class'ı eşleşmedi, yeni pattern olabilir!")

            time.sleep(1.7)
        except Exception as e:
            print(f"   ⚠️ Bir hata oluştu (bet {bet_num}): {e}")
            time.sleep(2.0)
    print("\n🎉 Tüm bahisler başarıyla tamamlandı!")

def test_dice_flow():
    driver, wait = open_browser()
    login_and_open_dice(driver, wait)
    play_10_bets(driver, wait)
    driver.quit()

if __name__ == "__main__":
    test_dice_flow()

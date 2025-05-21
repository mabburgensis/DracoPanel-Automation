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
    print("🚀 diamonds.py starting")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    # Login
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
        creds = load_user_data()
        print(f"DEBUG | User: {creds}")
        wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT))).send_keys(creds["username"])
        driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
        driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON).click()
        wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("✅ Login successful")
    except Exception as e:
        print(f"❌ Error during login: {e}")
        return False
    time.sleep(1.2)

    # Diamonds banner
    try:
        print("🎮 Clicking Diamonds banner...")
        banner = wait.until(EC.element_to_be_clickable((By.XPATH, DiamondsLocators.DIAMONDS_BANNER)))
        driver.execute_script("arguments[0].scrollIntoView(true);", banner)
        banner.click()
        print("DEBUG | Diamonds banner clicked.")
        time.sleep(1.2)
    except Exception as e:
        print(f"❌ Error clicking Diamonds banner: {e}")
        return False

    # Real Play
    try:
        print("▶️ Clicking Real Play...")
        real = wait.until(EC.element_to_be_clickable((By.XPATH, DiamondsLocators.REAL_PLAY_BUTTON)))
        real.click()
        print("DEBUG | Real Play clicked, game loading...")
    except Exception as e:
        print(f"❌ Error clicking Real Play: {e}")
        return False
    time.sleep(2.5)

    # Wait for the game to load
    print("⌛ Game is loading, waiting for bet input...")
    for attempt in range(1, 21):
        if switch_to_game_iframe(driver):
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, DiamondsLocators.BET_AMOUNT_INPUT)))
                print(f"✅ Game loaded! (on attempt {attempt})")
                return True
            except TimeoutException:
                print(f"DEBUG | Waiting for BET_AMOUNT_INPUT ({attempt}/20)...")
                time.sleep(0.7)
        else:
            print(f"DEBUG | Game iframe not ready yet ({attempt}/20)...")
            time.sleep(0.5)
    print("❌ Game could not be loaded! BET_AMOUNT_INPUT not found after 20 tries.")
    return False

def safe_input_and_click(driver, wait, input_xpath, value, button_xpath, retries=3):
    """
    Automatically retries on stale element and similar errors.
    """
    for attempt in range(retries):
        try:
            if not switch_to_game_iframe(driver):
                print(f"   ⚠️ ({attempt+1}/{retries}) Could not switch to game iframe, retrying...")
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
            print(f"   DEBUG | Bet input and button click successful (try {attempt+1})")
            return True
        except (StaleElementReferenceException, ElementNotInteractableException, TimeoutException) as e:
            print(f"   🔄 Retry ({attempt+1}/{retries}) | Error: {e}")
            time.sleep(1.2)
    print("   ❌ Could not access bet input or button (stabilization error)!")
    return False

def play_10_bets(driver, wait):
    print("🎲 10 random bets will be played…")
    for bet_num in range(1, 11):
        try:
            amount = random.randint(2, 99)
            print(f"   ➡️ ({bet_num}/10) Entering bet amount: {amount}")
            ok = safe_input_and_click(
                driver, wait,
                DiamondsLocators.BET_AMOUNT_INPUT,
                amount,
                DiamondsLocators.BET_SUBMIT_BUTTON,
                retries=4
            )
            if not ok:
                print("   ⚠️ Bet step skipped, moving to the next round.")
                continue

            print("   ✅ Bet submitted")
            time.sleep(2.0)

            switch_to_game_iframe(driver)
            try:
                win = wait.until(EC.presence_of_element_located((By.XPATH, DiamondsLocators.WIN_AMOUNT_INPUT)))
                multiplier = wait.until(EC.presence_of_element_located((By.XPATH, DiamondsLocators.MULTIPLIER_INPUT)))
                win_val = win.get_attribute('value')
                multiplier_val = multiplier.get_attribute('value')
                print(f"   🔎 Result: Win = {win_val}, Multiplier = {multiplier_val}")
            except TimeoutException:
                print("   ⚠️ Result field not found!")
            time.sleep(1.7)
        except Exception as e:
            print(f"   ⚠️ An error occurred (bet {bet_num}): {e}")
            time.sleep(2.0)
    print("\n🎉 All bets completed successfully!")

def test_diamonds_flow():
    driver, wait = open_browser()
    game_ready = login_and_open_diamonds(driver, wait)
    if not game_ready:
        print("❌ Game could not be loaded or login failed, test chain terminated.")
        driver.quit()
        return
    play_10_bets(driver, wait)
    time.sleep(2.0)
    driver.quit()

if __name__ == "__main__":
    test_diamonds_flow()
    sys.exit(0)

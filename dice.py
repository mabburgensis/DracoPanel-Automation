import time
import random
import sys
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
    print("🚀 dice.py is starting")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    # Login
    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
        print("DEBUG | Login button header clicked.")
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

    # Dice banner
    try:
        print("🎮 Clicking Dice banner...")
        banner = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.DICE_BANNER)))
        driver.execute_script("arguments[0].scrollIntoView(true);", banner)
        banner.click()
        print("DEBUG | Dice banner clicked.")
        time.sleep(1.2)
    except Exception as e:
        print(f"❌ Error clicking Dice banner: {e}")
        return False

    # Real Play
    try:
        print("▶️ Clicking Real Play...")
        real = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.REAL_PLAY_BUTTON)))
        real.click()
        print("DEBUG | Real Play clicked, game loading...")
    except Exception as e:
        print(f"❌ Error clicking Real Play: {e}")
        return False

    # After Real Play: wait for iframe + bet input
    print("⌛ Game is loading, waiting for bet input...")
    for _ in range(20):
        if switch_to_game_iframe(driver):
            try:
                wait.until(EC.visibility_of_element_located((By.XPATH, DiceLocators.BET_AMOUNT_INPUT)))
                print("✅ Game loaded!")
                return True
            except TimeoutException:
                print("DEBUG | Waiting for BET_AMOUNT_INPUT, will retry...")
                time.sleep(0.7)
        else:
            print("DEBUG | Game iframe not ready yet, will retry...")
            time.sleep(0.5)
    print("❌ Game could not be loaded! Input not found after 20 tries.")
    return False

def read_results_with_wait(driver, wait, timeout=5):
    # Results may appear late, retry up to 5 seconds
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
    print("🎲 10 random bets will be played…")
    for bet_num in range(1, 11):
        try:
            if not switch_to_game_iframe(driver):
                print("   ❌ Game iframe not found!")
                continue

            # Bet amount: integer between 1–99
            amount = random.randint(1, 99)
            amount_str = str(amount)
            print(f"   ➡️ ({bet_num}/10) Entering bet amount: {amount_str}")

            bet_input = wait.until(EC.element_to_be_clickable((By.XPATH, DiceLocators.BET_AMOUNT_INPUT)))
            bet_input.click()
            time.sleep(0.3)
            bet_input.send_keys(Keys.CONTROL, 'a')
            time.sleep(0.15)
            bet_input.send_keys(Keys.DELETE)
            time.sleep(0.3)
            slow_type(bet_input, amount_str, delay=0.13)
            time.sleep(1.1)

            # Chance (random integer between 1-99)
            chance = random.randint(1, 99)
            chance_str = str(chance)
            print(f"   ➡️ Entering Chance: {chance_str}")
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
            print("   ✅ Bet submitted")
            time.sleep(2.0)

            switch_to_game_iframe(driver)

            # Patient result read: log all history and new result
            result_buttons = read_results_with_wait(driver, wait, timeout=5)
            if not result_buttons:
                print("   ⚠️ Result button not found!")
            else:
                win_count = 0
                lose_count = 0
                for btn in result_buttons:
                    class_attr = btn.get_attribute("class") or ""
                    if "_won_" in class_attr:
                        print(f"   🟢 Win: {btn.text}")
                        win_count += 1
                    elif "_default_" in class_attr:
                        print(f"   🔴 Lose: {btn.text}")
                        lose_count += 1
                if win_count == 0 and lose_count == 0:
                    print("   ⚠️ Result class did not match, new pattern might be present!")

            time.sleep(1.7)
        except Exception as e:
            print(f"   ⚠️ An error occurred (bet {bet_num}): {e}")
            time.sleep(2.0)
    print("\n🎉 All bets completed successfully!")

def test_dice_flow():
    driver, wait = open_browser()
    game_ready = login_and_open_dice(driver, wait)
    if not game_ready:
        print("❌ Game never loaded or login failed, ending test chain.")
        driver.quit()
        return
    play_10_bets(driver, wait)
    driver.quit()

if __name__ == "__main__":
    test_dice_flow()
    sys.exit(0)

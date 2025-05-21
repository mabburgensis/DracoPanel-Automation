import time, random
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from common.browser_utils import open_browser
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.mines_locators import MinesLocators
from selenium.webdriver.common.keys import Keys

def switch_to_game_iframe(driver):
    print("DEBUG | switch_to_game_iframe called")
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        try:
            driver.switch_to.frame(iframe)
            print("DEBUG | Switched to an iframe, searching for bet input...")
            if driver.find_elements(By.XPATH, MinesLocators.BET_AMOUNT_INPUT):
                print("DEBUG | BET_AMOUNT_INPUT found, correct iframe")
                return True
        except Exception as e:
            print(f"DEBUG | iframe switch error: {e}")
        driver.switch_to.default_content()
    print("DEBUG | BET_AMOUNT_INPUT not found in any iframe")
    return False

def read_diamond_count(driver):
    print("DEBUG | read_diamond_count called")
    try:
        el = driver.find_element(By.XPATH, MinesLocators.DIAMONDS_INPUT)
        val = el.get_attribute("value") or el.get_property("value")
        print(f"DEBUG | Diamond value found: {val}")
        return int(float(val))
    except Exception as e:
        print(f"DEBUG | Diamond input could not be read: {e}")
        return None

def login_and_open_mines(driver, wait):
    print("DEBUG | login_and_open_mines STARTED")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    print("DEBUG | Waiting for Login button...")
    wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
    print("DEBUG | Login button clicked.")

    creds = load_user_data()
    print(f"DEBUG | User credentials loaded: {creds}")

    wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT))).send_keys(creds["username"])
    driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
    driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON).click()
    print("DEBUG | Login form filled and submitted.")

    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    print("DEBUG | Successfully logged in, LOGOUT_BUTTON found.")

    print("🎮 Clicking Mines banner...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    print("DEBUG | Mines banner clicked.")
    time.sleep(1)

    print("▶️ Clicking Real Play...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.REAL_PLAY_BUTTON)))
    real.click()
    print("DEBUG | Real Play clicked, game loading...")
    time.sleep(3)

def test_place_random_bet(driver, wait):
    # 1) Switch to iframe
    for i in range(3):
        print(f"DEBUG |- Switching to iframe attempt {i+1}...")
        if switch_to_game_iframe(driver):
            break
        time.sleep(1)
    else:
        print("DEBUG | test_place_random_bet: iframe not found, returning False")
        return False

    # 2) Find bet input
    try:
        print("DEBUG | Searching for BET_AMOUNT_INPUT...")
        bet_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.BET_AMOUNT_INPUT))
        )
    except TimeoutException:
        print("DEBUG | BET_AMOUNT_INPUT not found, TimeoutException")
        return False

    # 3) Enter random bet amount
    amt = random.randint(1, 99)
    print(f"DEBUG | Random bet: {amt}")
    bet_in.clear()
    time.sleep(0.5)
    bet_in.send_keys(str(amt))
    print(f"   🎲 Bet entered: {amt}")
    time.sleep(0.5)

    # 4) Wait for loader to disappear
    try:
        WebDriverWait(driver, 15).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div._loader_1g12d_17"))
        )
        print("DEBUG | Loader disappeared, select can be opened.")
    except Exception:
        print("WARN | Loader not found or took too long.")

    # 5) Wait for select to be enabled
    def wait_for_enabled(driver, locator, timeout=10):
        for _ in range(timeout * 2):
            el = driver.find_element(*locator)
            if el.is_enabled():
                return el
            time.sleep(0.5)
        raise Exception("Element not enabled!")

    mines_sel = wait_for_enabled(driver, (By.XPATH, MinesLocators.MINES_COUNT_SELECT))
    print("DEBUG | MINES_COUNT_SELECT being searched and clicked...")
    mines_sel.click()
    time.sleep(0.5)
    idx = random.randint(1, 24)
    print(f"DEBUG | Clicking option {idx} on MINES_COUNT_SELECT...")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"{MinesLocators.MINES_COUNT_SELECT}/option[{idx}]"))
    ).click()
    print(f"   💣 Bomb count: {idx}")
    time.sleep(0.5)

    print("DEBUG | Searching and clicking PLACE_BET_BUTTON...")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.PLACE_BET_BUTTON))
    ).click()
    print("   ✅ Bet submitted")
    time.sleep(2)
    return True

def play_until_first_win(driver, wait):
    print("DEBUG | play_until_first_win STARTED")
    while True:
        print("\n🔄 New round starting…")
        if not test_place_random_bet(driver, wait):
            print("DEBUG | test_place_random_bet failed, round restarting...")
            continue

        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before = read_diamond_count(driver)
        try:
            print("DEBUG | Searching for RANDOM_PICK_BUTTON (first pick)...")
            pick1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 First pick was a MINE, restarting")
            time.sleep(2)
            continue
        print("▶️ First pick is being clicked…")
        pick1.click()
        time.sleep(2)
        after1 = read_diamond_count(driver)
        if after1 is None or after1 >= (before or 0):
            print("💥 First pick was a MINE, restarting (no diamond or value didn't increase)")
            time.sleep(2)
            continue
        print("💎 First pick was a DIAMOND")

        # Second pick
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before2 = after1
        try:
            print("DEBUG | Searching for RANDOM_PICK_BUTTON (second pick)...")
            pick2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 Second pick button not found, restarting")
            time.sleep(2)
            continue
        print("▶️ Second pick is being clicked…")
        pick2.click()
        time.sleep(2)
        after2 = read_diamond_count(driver)
        if after2 is None or after2 >= before2:
            print("💥 Second pick was a MINE, restarting (no diamond or value didn't increase)")
            time.sleep(2)
            continue
        print("💎 Second pick was a DIAMOND")

        # Collect Winnings
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        try:
            print("DEBUG | Searching and clicking COLLECT_WIN_BUTTON...")
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.COLLECT_WIN_BUTTON))
            ).click()
            print("   ✅ Collect clicked")
        except Exception as e:
            print(f"DEBUG | Could not click Collect: {e}")
            break
        try:
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, MinesLocators.WIN_NOTIFICATION))
            )
            print(f"   🏆 {popup.text}")
        except TimeoutException:
            print("   ⚠️ No popup, still counted as success")
        print("🎉 First win collected, ending test!")
        break

def test_mines_flow():
    print("=== mines.py TEST STARTED ===")
    driver, wait = open_browser()
    print("DEBUG | open_browser finished")
    login_and_open_mines(driver, wait)
    print("DEBUG | login_and_open_mines finished")
    play_until_first_win(driver, wait)
    print("DEBUG | play_until_first_win finished")
    driver.quit()
    print("=== mines.py TEST FINISHED ===")

if __name__ == "__main__":
    test_mines_flow()
    sys.exit(0)

import time, random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from common.browser_utils import open_browser, screenshot
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.mines_locators import MinesLocators
from selenium.webdriver.common.keys import Keys

def switch_to_game_iframe(driver):
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        try:
            driver.switch_to.frame(iframe)
            if driver.find_elements(By.XPATH, MinesLocators.BET_AMOUNT_INPUT):
                return True
        except:
            pass
        driver.switch_to.default_content()
    return False

def read_diamond_count(driver):
    try:
        el = driver.find_element(By.XPATH, MinesLocators.DIAMONDS_INPUT)
        val = el.get_attribute("value") or el.get_property("value")
        return int(float(val))
    except:
        return None

def login_and_open_mines(driver, wait):
    print("🚀 mines.py başlatılıyor")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    # Login
    wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
    creds = load_user_data()
    wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))\
        .send_keys(creds["username"])
    driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
    driver.find_element(By.XPATH, LoginLocators.SUBMIT_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))

    # Mines banner
    print("🎮 Mines banner’a tıklanıyor...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    time.sleep(1)

    # Real Play
    print("▶️ Real Play’e tıklanıyor...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.REAL_PLAY_BUTTON)))
    real.click()
    time.sleep(3)
    screenshot(driver, "mines_game_opened")

def test_place_random_bet(driver, wait):
    for _ in range(3):
        if switch_to_game_iframe(driver):
            break
        time.sleep(1)
    else:
        return False

    try:
        bet_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.BET_AMOUNT_INPUT))
        )
    except TimeoutException:
        return False

    # --- Tam sayı random bahis (1-99), küsurat yok ---
    amt = random.randint(1, 99)
    bet_in.clear()
    time.sleep(0.5)
    bet_in.send_keys(str(amt))
    print(f"   🎲 Bet girildi: {amt}")
    time.sleep(0.5)

    mines_sel = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_COUNT_SELECT))
    )
    mines_sel.click()
    time.sleep(0.5)
    idx = random.randint(1, 24)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"{MinesLocators.MINES_COUNT_SELECT}/option[{idx}]"))
    ).click()
    print(f"   💣 Bomba sayısı: {idx}")
    time.sleep(0.5)

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.PLACE_BET_BUTTON))
    ).click()
    print("   ✅ Bahis gönderildi")
    screenshot(driver, "m01_bet_sent")
    time.sleep(2)
    return True

def play_until_first_win(driver, wait):
    """İlk kazanç sonrası test sonlandırılır."""
    while True:
        print("\n🔄 Yeni round başlıyor…")
        if not test_place_random_bet(driver, wait):
            continue

        # Birinci pick
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before = read_diamond_count(driver)
        try:
            pick1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 İlk pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("▶️ İlk pick tıklanıyor…")
        pick1.click()
        time.sleep(2)
        screenshot(driver, "after_first_pick")
        after1 = read_diamond_count(driver)
        if after1 is None or after1 >= (before or 0):
            print("💥 İlk pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("💎 İlk pick DIAMOND")

        # İkinci pick
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before2 = after1
        try:
            pick2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 İkinci pick butonu yok, yeniden başla")
            time.sleep(2)
            continue
        print("▶️ İkinci pick tıklanıyor…")
        pick2.click()
        time.sleep(2)
        screenshot(driver, "after_second_pick")
        after2 = read_diamond_count(driver)
        if after2 is None or after2 >= before2:
            print("💥 İkinci pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("💎 İkinci pick DIAMOND")

        # Collect Winnings (kazanç)
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.COLLECT_WIN_BUTTON))
        ).click()
        print("   ✅ Collect tıklandı")
        try:
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, MinesLocators.WIN_NOTIFICATION))
            )
            print(f"   🏆 {popup.text}")
        except TimeoutException:
            print("   ⚠️ Popup yok, yine de başarılı sayılıyor")
        screenshot(driver, "final_win_collected")
        print("🎉 İlk kazanç alındı, test sonlandırıldı!")
        break

def test_mines_flow():
    driver, wait = open_browser()
    login_and_open_mines(driver, wait)
    play_until_first_win(driver, wait)
    driver.quit()

if __name__ == "__main__":
    test_mines_flow()

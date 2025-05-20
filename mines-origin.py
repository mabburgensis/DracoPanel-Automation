
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import random

from common.browser_utils import open_browser, screenshot
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.mines_locators import MinesLocators


def switch_to_game_iframe(driver):
    print("🧭 IFrame'e geçiliyor...")
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"🔍 Toplam iframe sayısı: {len(iframes)}")
    for index, iframe in enumerate(iframes):
        try:
            driver.switch_to.frame(iframe)
            if driver.find_elements(By.XPATH, MinesLocators.BET_AMOUNT_INPUT):
                print(f"✅ BET_AMOUNT_INPUT bulundu -> iframe index: {index}")
                return True
            driver.switch_to.default_content()
        except Exception as e:
            print(f"⚠️ iframe switch hatası: {e}")
    print("❌ BET_AMOUNT_INPUT bulunamadı. Devam edilemiyor.")
    return False


def login_and_open_mines(driver, wait):
    print("🚀 Başlatılıyor: mines.py")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER)))
    login_btn.click()
    time.sleep(1)

    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))
    credentials = load_user_data()

    username = driver.find_element(By.XPATH, LoginLocators.USERNAME_INPUT)
    password = driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT)
    submit = driver.find_element(By.XPATH, LoginLocators.SUBMIT_BUTTON)

    username.send_keys(credentials["username"])
    time.sleep(1)
    password.send_keys(credentials["password"])
    time.sleep(1)
    submit.click()

    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    print("🟢 Login başarılı")
    time.sleep(1)

    mines_banner = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView();", mines_banner)
    time.sleep(0.5)
    mines_banner.click()
    print("🟢 Mines oyun ekranı açıldı")
    time.sleep(4)
    screenshot(driver, "mines_game_opened")


def test_manual_mode_and_grid_play(driver, wait):
    print("🎯 M-01: Manuel bahis + grid + rastgele seçim + kazancı topla")

    if not switch_to_game_iframe(driver):
        return

    # Bahis ayarı
    bet_input = wait.until(EC.visibility_of_element_located((By.XPATH, MinesLocators.BET_AMOUNT_INPUT)))
    bet_input.clear()
    time.sleep(1)
    bet_input.send_keys("0.10")
    time.sleep(1)

    mine_select = driver.find_element(By.XPATH, MinesLocators.MINES_COUNT_SELECT)
    mine_select.click()
    time.sleep(1)
    mine_select.find_element(By.XPATH, './option[2]').click()
    time.sleep(1)

    place_bet = driver.find_element(By.XPATH, MinesLocators.PLACE_BET_BUTTON)
    place_bet.click()
    time.sleep(2)
    print("✅ Bahis gönderildi.")

    # Grid tıklama
    canvas = wait.until(EC.visibility_of_element_located((By.XPATH, MinesLocators.GAME_BOARD_CANVAS)))
    action = ActionChains(driver)
    rand_x = random.randint(50, 300)
    rand_y = random.randint(50, 300)
    action.move_to_element_with_offset(canvas, rand_x, rand_y).click().perform()
    print(f"🟢 Grid tıklandı ({rand_x}, {rand_y})")
    time.sleep(3)

    # Kazanç kontrol
    try:
        collect_btn = driver.find_element(By.XPATH, MinesLocators.COLLECT_PROFIT_BUTTON)
        if collect_btn.is_enabled():
            collect_btn.click()
            print("🟢 Kazanç toplandı.")
            time.sleep(2)
            return
    except:
        pass

    # Rastgele Seç
    try:
        rand_btn = driver.find_element(By.XPATH, MinesLocators.RANDOM_PICK_BUTTON)
        if rand_btn.is_enabled():
            rand_btn.click()
            print("🟢 Rastgele Seç tıklandı.")
            time.sleep(2)

            # Kazanç tekrar kontrol
            try:
                collect_btn = driver.find_element(By.XPATH, MinesLocators.COLLECT_PROFIT_BUTTON)
                if collect_btn.is_enabled():
                    collect_btn.click()
                    print("🟢 Kazanç toplandı.")
                    time.sleep(2)
            except:
                print("⚠️ Kazanç topla butonu yok.")
    except:
        print("❌ Rastgele Seç butonu bulunamadı.")


def test_auto_mode_play(driver, wait):
    print("🎯 M-04: Auto mod ile bahis başlatılıyor")
    auto_tab = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_TAB_BUTTON)))
    auto_tab.click()
    time.sleep(1)

    auto_bet_amount = wait.until(EC.presence_of_element_located((By.XPATH, MinesLocators.AUTO_BET_AMOUNT_INPUT)))
    auto_bet_amount.clear()
    auto_bet_amount.send_keys("0.10")
    time.sleep(1)

    auto_bet_count = driver.find_element(By.XPATH, MinesLocators.AUTO_BET_COUNT_INPUT)
    auto_bet_count.clear()
    auto_bet_count.send_keys("1")
    time.sleep(1)

    auto_play_btn = driver.find_element(By.XPATH, MinesLocators.AUTO_PLAY_BUTTON)
    auto_play_btn.click()
    print("✅ Otomatik bahis başlatıldı")
    screenshot(driver, "m04_auto_play_started")
    time.sleep(2)


def test_mines_flow():
    driver, wait = open_browser()
    login_and_open_mines(driver, wait)

    if switch_to_game_iframe(driver):
        test_manual_mode_and_grid_play(driver, wait)
        test_auto_mode_play(driver, wait)

    input("\n🔵 Mines test tamamlandı. Tarayıcıyı kapatmak için Enter'a bas...")
    # driver.quit()


if __name__ == "__main__":
    test_mines_flow()

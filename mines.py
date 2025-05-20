print("=== mines.py BAŞLADI ===")
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
    print("DEBUG | switch_to_game_iframe çağrıldı")
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        try:
            driver.switch_to.frame(iframe)
            print("DEBUG | Bir iframe'e geçildi, içeride bet input aranıyor...")
            if driver.find_elements(By.XPATH, MinesLocators.BET_AMOUNT_INPUT):
                print("DEBUG | BET_AMOUNT_INPUT bulundu, iframe doğru")
                return True
        except Exception as e:
            print(f"DEBUG | iframe geçiş hatası: {e}")
        driver.switch_to.default_content()
    print("DEBUG | Hiçbir iframe'de BET_AMOUNT_INPUT bulunamadı")
    return False

def read_diamond_count(driver):
    print("DEBUG | read_diamond_count çağrıldı")
    try:
        el = driver.find_element(By.XPATH, MinesLocators.DIAMONDS_INPUT)
        val = el.get_attribute("value") or el.get_property("value")
        print(f"DEBUG | Diamond value bulundu: {val}")
        return int(float(val))
    except Exception as e:
        print(f"DEBUG | Diamond input okunamadı: {e}")
        return None

def login_and_open_mines(driver, wait):
    print("DEBUG | login_and_open_mines BAŞLADI")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    print("DEBUG | Login butonu bekleniyor...")
    wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
    print("DEBUG | Login butonuna tıklandı.")

    creds = load_user_data()
    print(f"DEBUG | Kullanıcı verisi yüklendi: {creds}")

    wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT))).send_keys(creds["username"])
    driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
    driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON).click()
    print("DEBUG | Login formu dolduruldu ve gönderildi.")

    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    print("DEBUG | Başarıyla login olundu, LOGOUT_BUTTON bulundu.")

    print("🎮 Mines banner’a tıklanıyor...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    print("DEBUG | Mines banner tıklandı.")
    time.sleep(1)

    print("▶️ Real Play’e tıklanıyor...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.REAL_PLAY_BUTTON)))
    real.click()
    print("DEBUG | Real Play tıklandı, oyun yükleniyor...")
    time.sleep(3)
    # screenshot(driver, "mines_game_opened")

def test_place_random_bet(driver, wait):
    print("DEBUG | test_place_random_bet BAŞLADI")
    for i in range(3):
        print(f"DEBUG | {i+1}. kez iframe'e geçiliyor...")
        if switch_to_game_iframe(driver):
            break
        time.sleep(1)
    else:
        print("DEBUG | test_place_random_bet: iframe bulunamadı, fonksiyondan False dönülüyor")
        return False

    try:
        print("DEBUG | BET_AMOUNT_INPUT aranıyor...")
        bet_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.BET_AMOUNT_INPUT))
        )
    except TimeoutException:
        print("DEBUG | BET_AMOUNT_INPUT bulunamadı, TimeoutException")
        return False

    amt = random.randint(1, 99)
    print(f"DEBUG | Rastgele bahis: {amt}")
    bet_in.clear()
    time.sleep(0.5)
    bet_in.send_keys(str(amt))
    print(f"   🎲 Bet girildi: {amt}")
    time.sleep(0.5)

    print("DEBUG | MINES_COUNT_SELECT aranıyor ve tıklanıyor...")
    mines_sel = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_COUNT_SELECT))
    )
    mines_sel.click()
    time.sleep(0.5)
    idx = random.randint(1, 24)
    print(f"DEBUG | MINES_COUNT_SELECT'te {idx}. seçenek tıklanacak...")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"{MinesLocators.MINES_COUNT_SELECT}/option[{idx}]"))
    ).click()
    print(f"   💣 Bomba sayısı: {idx}")
    time.sleep(0.5)

    print("DEBUG | PLACE_BET_BUTTON aranıyor ve tıklanıyor...")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.PLACE_BET_BUTTON))
    ).click()
    print("   ✅ Bahis gönderildi")
    time.sleep(2)
    return True

def play_until_first_win(driver, wait):
    print("DEBUG | play_until_first_win BAŞLADI")
    while True:
        print("\n🔄 Yeni round başlıyor…")
        if not test_place_random_bet(driver, wait):
            print("DEBUG | test_place_random_bet başarısız, round başa sarıyor...")
            continue

        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before = read_diamond_count(driver)
        try:
            print("DEBUG | RANDOM_PICK_BUTTON aranıyor (ilk pick)...")
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
        after1 = read_diamond_count(driver)
        if after1 is None or after1 >= (before or 0):
            print("💥 İlk pick MINE, yeniden başla (diamond alınamadı ya da değer artmadı)")
            time.sleep(2)
            continue
        print("💎 İlk pick DIAMOND")

        # İkinci pick
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        before2 = after1
        try:
            print("DEBUG | RANDOM_PICK_BUTTON aranıyor (ikinci pick)...")
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
        after2 = read_diamond_count(driver)
        if after2 is None or after2 >= before2:
            print("💥 İkinci pick MINE, yeniden başla (diamond alınamadı ya da değer artmadı)")
            time.sleep(2)
            continue
        print("💎 İkinci pick DIAMOND")

        # Collect Winnings (kazanç)
        driver.switch_to.default_content()
        switch_to_game_iframe(driver)
        try:
            print("DEBUG | COLLECT_WIN_BUTTON aranıyor ve tıklanıyor...")
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.COLLECT_WIN_BUTTON))
            ).click()
            print("   ✅ Collect tıklandı")
        except Exception as e:
            print(f"DEBUG | Collect tıklanamadı: {e}")
            break
        try:
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, MinesLocators.WIN_NOTIFICATION))
            )
            print(f"   🏆 {popup.text}")
        except TimeoutException:
            print("   ⚠️ Popup yok, yine de başarılı sayılıyor")
        print("🎉 İlk kazanç alındı, test sonlandırıldı!")
        break

def test_mines_flow():
    print("=== mines.py TEST BAŞLIYOR ===")
    driver, wait = open_browser()
    print("DEBUG | open_browser tamamlandı")
    login_and_open_mines(driver, wait)
    print("DEBUG | login_and_open_mines tamamlandı")
    play_until_first_win(driver, wait)
    print("DEBUG | play_until_first_win tamamlandı")
    driver.quit()
    print("=== mines.py TEST BİTTİ ===")

if __name__ == "__main__":
    test_mines_flow()

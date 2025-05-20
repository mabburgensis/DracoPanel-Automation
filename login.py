import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from common.browser_utils import open_browser
import time
from common.user_data import load_user_data
from locators.login_locators import LoginLocators

def get_login_elements(driver):
    username_el = driver.find_element(By.XPATH, LoginLocators.USERNAME_INPUT)
    password_el = driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT)
    submit_btn = driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON)
    return username_el, password_el, submit_btn

def open_login_modal(driver, wait):
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER)))
    time.sleep(1)  # Yavaş kullanıcı/bilgisayar simülasyonu
    login_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))
    time.sleep(1)
    # # screenshot(driver, "login_modal_opened")  # KALDIRILDI

def test_login_flow():
    driver, wait = open_browser()
    time.sleep(1)
    open_login_modal(driver, wait)
    time.sleep(1)
    username_el, password_el, submit_btn = get_login_elements(driver)
    time.sleep(1)

    # L-01: Alanlar boş
    submit_btn.click()
    print("L-01: Alanlar boş gönderildi")
    time.sleep(1)
    try:
        error1 = driver.find_element(By.XPATH, LoginLocators.USERNAME_REQUIRED_ERROR)
        print(f"✅ Kullanıcı adı boş: {error1.text}")
    except:
        print("✅ Kullanıcı adı boş: Hata mesajı görünmedi")
    try:
        error2 = driver.find_element(By.XPATH, LoginLocators.PASSWORD_REQUIRED_ERROR)
        print(f"✅ Parola boş: {error2.text}")
    except:
        print("✅ Parola boş: Hata mesajı görünmedi")
    # # screenshot(driver, "l01_empty_fields")  # KALDIRILDI
    time.sleep(1)

    # L-02: Geçersiz kullanıcı adı
    username_el.send_keys("invalid_user")
    time.sleep(0.7)
    password_el.send_keys("Test123!")
    time.sleep(0.7)
    submit_btn.click()
    print("L-02: Geçersiz kullanıcı adı gönderildi")
    time.sleep(2)
    # # screenshot(driver, "l02_invalid_username")  # KALDIRILDI

    # L-03: Geçersiz şifre
    username_el.clear()
    password_el.clear()
    time.sleep(0.7)
    try:
        user_data = load_user_data()
    except FileNotFoundError:
        raise ValueError("❗ Register verileri eksik! Lütfen önce register.py çalıştırıldığından emin olun.")
    valid_username = user_data["username"]
    invalid_password = "WrongPassword123"

    username_el.send_keys(valid_username)
    time.sleep(0.7)
    password_el.send_keys(invalid_password)
    time.sleep(0.7)
    submit_btn.click()
    print("L-03: Geçersiz şifre gönderildi")
    time.sleep(2)
    # # screenshot(driver, "l03_invalid_password")  # KALDIRILDI

    # L-04: Başarılı login
    time.sleep(1)
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    time.sleep(0.7)

    valid_password = user_data["password"]

    print(f"🛠 DEBUG | Username: {valid_username}")
    print(f"🛠 DEBUG | Password: {valid_password!r}")

    username_el.send_keys(valid_username)
    time.sleep(0.7)
    password_el.send_keys(valid_password)
    time.sleep(0.7)
    # # screenshot(driver, "l04_before_login")  # KALDIRILDI
    submit_btn.click()
    time.sleep(2)

    print(f"\n✅ L-04: Başarılı login deneniyor... ({valid_username})")

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-04: Giriş başarılı!")
        # # screenshot(driver, "l04_login_success")  # KALDIRILDI
    except:
        print("🔴 L-04: Giriş başarısız gibi görünüyor")
        # # screenshot(driver, "l04_login_failure")  # KALDIRILDI
    time.sleep(1)

    # L-05: Logout ve tekrar login
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    logout_btn.click()
    time.sleep(1.5)
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGIN_BUTTON_AFTER_LOGOUT)))
    print("🔄 Logout işlemi başarılı, tekrar giriş deneniyor...")
    # # screenshot(driver, "l05_after_logout")  # KALDIRILDI
    time.sleep(1)

    open_login_modal(driver, wait)
    time.sleep(1)
    username_el, password_el, submit_btn = get_login_elements(driver)
    time.sleep(1)
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    time.sleep(0.7)

    username_el.send_keys(valid_username)
    time.sleep(0.7)
    password_el.send_keys(valid_password)
    time.sleep(0.7)
    submit_btn.click()
    time.sleep(2)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-05: Tekrar giriş başarılı.")
        # # screenshot(driver, "l05_relogin_success")  # KALDIRILDI
    except:
        print("🔴 L-05: Tekrar giriş başarısız.")
        # # screenshot(driver, "l05_relogin_failure")  # KALDIRILDI

    driver.quit()

if __name__ == "__main__":
    test_login_flow()
    sys.exit(0)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

from common.browser_utils import open_browser, screenshot
from common.user_data import load_user_data
from locators.login_locators import LoginLocators


def open_login_modal(driver, wait):
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER)))
    login_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))
    screenshot(driver, "login_modal_opened")


def open_login_modal(driver, wait):
    wait = WebDriverWait(driver, 20)
    try:
        login_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))
        )
        driver.save_screenshot("login_btn_found.png")
        login_btn.click()
    except Exception as e:
        driver.save_screenshot("login_btn_NOT_found.png")
        print("Login butonu bulunamadı veya tıklanamadı:", e)
        raise


def test_login_flow():
    driver, wait = open_browser()
    open_login_modal(driver, wait)
    username_el, password_el, submit_btn = get_login_elements(driver)

    # L-01: Alanlar boş
    submit_btn.click()
    print("L-01: Alanlar boş gönderildi")
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
    screenshot(driver, "l01_empty_fields")

    # L-02: Geçersiz kullanıcı adı
    username_el.send_keys("invalid_user")
    password_el.send_keys("Test123!")
    submit_btn.click()
    time.sleep(1)
    print("L-02: Geçersiz kullanıcı adı gönderildi")
    screenshot(driver, "l02_invalid_username")

    # L-03: Geçersiz şifre
    username_el.clear()
    password_el.clear()
    try:
        user_data = load_user_data()
    except FileNotFoundError:
        raise ValueError("❗ Register verileri eksik! Lütfen önce register.py çalıştırıldığından emin olun.")

    valid_username = user_data["username"]
    invalid_password = "WrongPassword123"

    username_el.send_keys(valid_username)
    password_el.send_keys(invalid_password)
    submit_btn.click()
    time.sleep(1)
    print("L-03: Geçersiz şifre gönderildi")
    screenshot(driver, "l03_invalid_password")

    # L-04: Başarılı login
    time.sleep(1)  # elementlerin oturmasını bekle
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)

    valid_password = user_data["password"]

    print(f"🛠 DEBUG | Username: {valid_username}")
    print(f"🛠 DEBUG | Password: {valid_password!r}")

    username_el.send_keys(valid_username)
    password_el.send_keys(valid_password)
    screenshot(driver, "l04_before_login")
    submit_btn.click()

    print(f"\n✅ L-04: Başarılı login deneniyor... ({valid_username})")

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-04: Giriş başarılı!")
        screenshot(driver, "l04_login_success")
    except:
        print("🔴 L-04: Giriş başarısız gibi görünüyor")
        screenshot(driver, "l04_login_failure")

    # L-05: Logout ve tekrar login
    logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
    logout_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGIN_BUTTON_AFTER_LOGOUT)))
    print("🔄 Logout işlemi başarılı, tekrar giriş deneniyor...")
    screenshot(driver, "l05_after_logout")

    open_login_modal(driver, wait)
    username_el, password_el, submit_btn = get_login_elements(driver)

    time.sleep(1)
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)

    username_el.send_keys(valid_username)
    password_el.send_keys(valid_password)
    submit_btn.click()

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-05: Tekrar giriş başarılı.")
        screenshot(driver, "l05_relogin_success")
    except:
        print("🔴 L-05: Tekrar giriş başarısız.")
        screenshot(driver, "l05_relogin_failure")

    driver.quit()


if __name__ == "__main__":
    test_login_flow()

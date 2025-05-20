from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random

from common.browser_utils import open_browser, screenshot
from locators.register_locators import RegisterLocators
from common import user_data  # ✅ JSON dosyasına veri kaydı için


def open_register_modal(driver, wait):
    register_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, RegisterLocators.REGISTER_BUTTON)
    ))
    register_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, RegisterLocators.EMAIL_INPUT)))
    screenshot(driver, "register_modal_opened")


def get_form_elements(driver):
    email = driver.find_element(By.XPATH, RegisterLocators.EMAIL_INPUT)
    username = driver.find_element(By.XPATH, RegisterLocators.USERNAME_INPUT)
    password = driver.find_element(By.XPATH, RegisterLocators.PASSWORD_INPUT)
    submit = driver.find_element(By.XPATH, RegisterLocators.SUBMIT_BUTTON)
    return email, username, password, submit


def print_error(driver, xpath, label, ss_name):
    try:
        error = driver.find_element(By.XPATH, xpath)
        print(f"❌ {label}: {error.text}")
        screenshot(driver, ss_name)
    except:
        print(f"✅ {label}: Hata mesajı görünmedi")
        screenshot(driver, ss_name + "_noerror")


def test_registration_flow():
    driver, wait = open_browser()
    open_register_modal(driver, wait)

    email, username, password, submit = get_form_elements(driver)

    # R-01: Tüm alanlar boş
    submit.click()
    time.sleep(1)
    print("\nR-01: Alanlar boş gönderildi")
    print_error(driver, RegisterLocators.EMAIL_REQUIRED_ERROR, "E-posta alanı boş", "r01_email_required")
    print_error(driver, RegisterLocators.USERNAME_REQUIRED_ERROR, "Kullanıcı adı boş", "r01_username_required")
    print_error(driver, RegisterLocators.PASSWORD_REQUIRED_ERROR, "Parola boş", "r01_password_required")

    # R-02: Geçersiz e-posta
    email.send_keys("asdsad")
    submit.click()
    time.sleep(1)
    print("\nR-02: Geçersiz e-posta gönderildi")
    print_error(driver, RegisterLocators.EMAIL_INVALID_ERROR, "E-posta biçimi geçersiz", "r02_invalid_email")

    # R-03: Geçerli kayıt
    email.clear()
    username.clear()
    password.clear()

    valid_email = f"test{random.randint(1000,9999)}@mail.com"
    valid_username = f"user{random.randint(1000,9999)}"
    password_val = "Test123!"

    # login.py tarafından kullanılacak verileri JSON dosyasına kaydet
    user_data.save_user_data(valid_email, valid_username, password_val)

    email.send_keys(valid_email)
    username.send_keys(valid_username)
    password.send_keys(password_val)

    screenshot(driver, "r03_before_submit")
    submit.click()
    print(f"\n✅ R-03: Başarılı kayıt deneniyor... ({valid_email}, {valid_username})")

    try:
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, RegisterLocators.REGISTER_MODAL_FORM)
        ))
        print("🟢 R-03: Kayıt başarıyla tamamlandı.")
        screenshot(driver, "r03_success")
    except:
        print("🔴 R-03: Kayıt başarısız gibi görünüyor (modal kapanmadı).")
        screenshot(driver, "r03_failure")

    time.sleep(5)
    screenshot(driver, "r03_after_submit")
    driver.quit()  # Şimdilik kapalı


if __name__ == "__main__":
    test_registration_flow()

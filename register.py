from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import sys
from pathlib import Path
from common.browser_utils import open_browser
from locators.register_locators import RegisterLocators
from common import user_data  # For saving test user data to JSON

TEST_USER_DATA_FILE = "test_user_data.json"

def open_register_modal(driver, wait):
    print("DEBUG | Opening registration modal...")
    register_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, RegisterLocators.REGISTER_BUTTON)
    ))
    register_btn.click()
    wait.until(EC.presence_of_element_located((By.XPATH, RegisterLocators.EMAIL_INPUT)))
    print("DEBUG | Registration modal opened.")

def get_form_elements(driver):
    print("DEBUG | Getting form input elements...")
    email = driver.find_element(By.XPATH, RegisterLocators.EMAIL_INPUT)
    username = driver.find_element(By.XPATH, RegisterLocators.USERNAME_INPUT)
    password = driver.find_element(By.XPATH, RegisterLocators.PASSWORD_INPUT)
    submit = driver.find_element(By.XPATH, RegisterLocators.SUBMIT_BUTTON)
    return email, username, password, submit

def print_error(driver, xpath, label, ss_name):
    try:
        error = driver.find_element(By.XPATH, xpath)
        print(f"❌ {label}: {error.text}")
    except:
        print(f"✅ {label}: No error message displayed")

def test_registration_flow():
    driver, wait = open_browser()
    open_register_modal(driver, wait)
    email, username, password, submit = get_form_elements(driver)

    # R-01: All fields empty
    submit.click()
    time.sleep(1)
    print("\nR-01: Submitted with empty fields")
    print_error(driver, RegisterLocators.EMAIL_REQUIRED_ERROR, "Email field empty", "r01_email_required")
    print_error(driver, RegisterLocators.USERNAME_REQUIRED_ERROR, "Username field empty", "r01_username_required")
    print_error(driver, RegisterLocators.PASSWORD_REQUIRED_ERROR, "Password field empty", "r01_password_required")

    # R-02: Invalid email
    email.send_keys("asdsad")
    submit.click()
    time.sleep(1)
    print("\nR-02: Submitted with invalid email")
    print_error(driver, RegisterLocators.EMAIL_INVALID_ERROR, "Invalid email format", "r02_invalid_email")

    # R-03: Valid registration
    email.clear()
    username.clear()
    password.clear()

    valid_email = f"test{random.randint(1000,9999)}@mail.com"
    valid_username = f"user{random.randint(1000,9999)}"
    password_val = "Test123!"

    print(f"\nDEBUG | Generated valid data: {valid_email}, {valid_username}, {password_val}")

    # Save user data to test_user_data.json
    user_data.save_user_data(valid_email, valid_username, password_val)
    print(f"DEBUG | Test user data saved: {TEST_USER_DATA_FILE}")

    # Assert that file was actually created
    assert Path(TEST_USER_DATA_FILE).exists(), f"ASSERT FAILED | {TEST_USER_DATA_FILE} could not be saved!"
    print(f"ASSERT PASSED | {TEST_USER_DATA_FILE} file exists.")

    email.send_keys(valid_email)
    username.send_keys(valid_username)
    password.send_keys(password_val)

    submit.click()
    print(f"\n✅ R-03: Trying valid registration... ({valid_email}, {valid_username})")

    try:
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, RegisterLocators.REGISTER_MODAL_FORM)
        ))
        print("🟢 R-03: Registration successful.")
    except Exception as e:
        print("🔴 R-03: Registration seems failed (modal did not close).")
        print(f"DEBUG | Error waiting for modal to close: {e}")

    # Final check: Read data from file and assert
    try:
        data = user_data.load_user_data()
        assert data["email"] == valid_email, "ASSERT FAILED | Email was saved differently!"
        assert data["username"] == valid_username, "ASSERT FAILED | Username was saved differently!"
        assert data["password"] == password_val, "ASSERT FAILED | Password was saved differently!"
        print("ASSERT PASSED | Test data was successfully read and verified from file.")
    except Exception as e:
        print(f"ASSERT FAILED | Test data could not be read from file or data mismatch: {e}")

    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    test_registration_flow()
    sys.exit(0)

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
    print("DEBUG | get_login_elements called")
    username_el = driver.find_element(By.XPATH, LoginLocators.USERNAME_INPUT)
    password_el = driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT)
    submit_btn = driver.find_element(By.XPATH, LoginLocators.LOGIN_SUBMIT_BUTTON)
    return username_el, password_el, submit_btn

def open_login_modal(driver, wait):
    print("DEBUG | open_login_modal called")
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER)))
    time.sleep(0.7)
    login_btn.click()
    print("DEBUG | Login modal opened, waiting for username input")
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))
    time.sleep(0.7)

def test_login_flow():
    print("=== login.py TEST STARTED ===")
    driver, wait = open_browser()
    time.sleep(1)
    open_login_modal(driver, wait)
    time.sleep(1)
    username_el, password_el, submit_btn = get_login_elements(driver)
    time.sleep(0.5)

    # L-01: Empty fields
    submit_btn.click()
    print("L-01: Submitted with empty fields")
    time.sleep(0.7)
    try:
        error1 = driver.find_element(By.XPATH, LoginLocators.USERNAME_REQUIRED_ERROR)
        print(f"✅ Username empty: {error1.text}")
    except Exception as e:
        print("✅ Username empty: No error message displayed")
    try:
        error2 = driver.find_element(By.XPATH, LoginLocators.PASSWORD_REQUIRED_ERROR)
        print(f"✅ Password empty: {error2.text}")
    except Exception as e:
        print("✅ Password empty: No error message displayed")
    time.sleep(0.7)

    # L-02: Invalid username
    username_el.send_keys("invalid_user")
    time.sleep(0.5)
    password_el.send_keys("Test123!")
    time.sleep(0.5)
    submit_btn.click()
    print("L-02: Submitted with invalid username")
    time.sleep(1.2)

    # L-03: Invalid password
    username_el.clear()
    password_el.clear()
    time.sleep(0.5)
    try:
        user_data = load_user_data()
        print(f"DEBUG | user_data loaded: {user_data}")
    except FileNotFoundError:
        raise ValueError("❗ Register data is missing! Please make sure to run register.py first.")

    valid_username = user_data["username"]
    invalid_password = "WrongPassword123"

    username_el.send_keys(valid_username)
    time.sleep(0.4)
    password_el.send_keys(invalid_password)
    time.sleep(0.4)
    submit_btn.click()
    print("L-03: Submitted with invalid password")
    time.sleep(1.2)

    # L-04: Successful login
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    time.sleep(0.5)

    valid_password = user_data["password"]

    print(f"🛠 DEBUG | Username: {valid_username}")
    print(f"🛠 DEBUG | Password: {valid_password!r}")

    username_el.send_keys(valid_username)
    time.sleep(0.4)
    password_el.send_keys(valid_password)
    time.sleep(0.4)
    submit_btn.click()
    print(f"\n✅ L-04: Attempting successful login... ({valid_username})")
    time.sleep(1.4)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-04: Login successful!")
    except Exception as e:
        print(f"🔴 L-04: Login seems failed | Error: {e}")
    time.sleep(0.7)

    # L-05: Logout and login again
    try:
        logout_btn = wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        logout_btn.click()
        time.sleep(1.1)
        wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGIN_BUTTON_AFTER_LOGOUT)))
        print("🔄 Logout successful, trying login again...")
    except Exception as e:
        print(f"❌ Error during logout: {e}")

    open_login_modal(driver, wait)
    time.sleep(0.7)
    username_el, password_el, submit_btn = get_login_elements(driver)
    username_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    password_el.send_keys(Keys.CONTROL + 'a', Keys.DELETE)
    time.sleep(0.4)

    username_el.send_keys(valid_username)
    time.sleep(0.4)
    password_el.send_keys(valid_password)
    time.sleep(0.4)
    submit_btn.click()
    print("L-05: Trying to login again")
    time.sleep(1.5)

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGOUT_BUTTON)))
        print("🟢 L-05: Login again successful.")
    except Exception as e:
        print(f"🔴 L-05: Login again failed. | Error: {e}")

    driver.quit()
    print("=== login.py TEST FINISHED ===")

if __name__ == "__main__":
    test_login_flow()
    sys.exit(0)

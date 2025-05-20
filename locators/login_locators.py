class LoginLocators:
    LOGIN_BUTTON_HEADER = '//*[@id="root"]/main/header/div/nav[2]/button[1]'
    USERNAME_INPUT = '//*[@id="root"]/div[2]/div/section/div/form/div/label[1]/input'
    PASSWORD_INPUT = '//*[@id="root"]/div[2]/div/section/div/form/div/label[2]/input'
    LOGIN_SUBMIT_BUTTON = '//*[@id="root"]/div[2]/div/section/div/form/button'

    USERNAME_REQUIRED_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[1]/p'
    PASSWORD_REQUIRED_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[2]/p'

    ERROR_MESSAGE_BOX = '/html/body/div/div/div[2]'

    LOGOUT_BUTTON = '//*[@id="root"]/main/header/div/div/button'
    LOGIN_BUTTON_AFTER_LOGOUT = '//*[@id="root"]/main/header/div/nav[2]/button[1]'
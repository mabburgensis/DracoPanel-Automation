# locators/register_locators.py

class RegisterLocators:
    REGISTER_BUTTON = '//*[@id="root"]/main/header/div/nav[2]/button[2]'
    EMAIL_INPUT = '//*[@id="root"]/div[2]/div/section/div/form/div/label[1]/input'
    USERNAME_INPUT = '//*[@id="root"]/div[2]/div/section/div/form/div/label[2]/input'
    PASSWORD_INPUT = '//*[@id="root"]/div[2]/div/section/div/form/div/label[3]/input'
    SUBMIT_BUTTON = '//*[@id="root"]/div[2]/div/section/div/form/div/button'
    
    EMAIL_REQUIRED_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[1]/p'
    EMAIL_INVALID_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[1]/p'
    USERNAME_REQUIRED_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[2]/p'
    PASSWORD_REQUIRED_ERROR = '//*[@id="root"]/div[2]/div/section/div/form/div/label[3]/p'
    REGISTER_MODAL_FORM = '//*[@id="root"]/div[2]/div/section/div/form'
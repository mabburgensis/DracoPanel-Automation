# dice_locators.py

class DiceLocators:

    DICE_BANNER = '//*[@id="root"]/main/div/div[2]/div/div[2]/a[6]/img'
    
    # Oyun açılış ve iframe
    REAL_PLAY_BUTTON      = '//*[@id="root"]/main/div/div/div/button[1]'
    GAME_IFRAME           = '//iframe[contains(@src, "dice")]'  # src'de "dice" geçen ilk iframe, gerekirse değiştir

    # Bahis Paneli
    MANUAL_TAB_BUTTON     = '//*[@id="root"]/div/aside/section/nav/button[1]'
    BET_AMOUNT_INPUT      = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    BET_SUBMIT_BUTTON     = '//*[@id="root"]/div/aside/section/section/button'

    # Slider ve Scoreboard
    SLIDER_CANVAS         = '//*[@id="root"]/div/div/canvas'
    SCOREBOARD_ROOT       = '//*[@id="root"]/div/div/div[1]'
    MULTIPLIER_INPUT      = '//*[@id="root"]/div/div/div[1]/div[1]/div/div[2]/div/input'
    OVER_INPUT            = '//*[@id="root"]/div/div/div[1]/div[1]/div/div[2]/div/input'  # Tekrar kontrol edebilirsin
    CHANCE_INPUT          = '//*[@id="root"]/div/div/div[1]/div[3]/div/div[2]/div/input'

    # Sonuç/Kazanç paneli
    RESULT_ROOT_DIV       = '//*[@id="root"]/div/div/div[2]'
    WIN_AMOUNT_BUTTON     = '//*[@id="root"]/div/div/div[2]/button[1]'
    LOSS_AMOUNT_BUTTON    = '//*[@id="root"]/div/div/div[2]/button[4]'

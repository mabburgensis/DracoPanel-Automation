# locators/mines_locators.py

class MinesLocators:
    # Oyuna giriş için banner
    MINES_BANNER = '//*[@id="root"]/main/div/div[2]/div/div[2]/a[5]/img'

    # Manuel mod inputları
    BET_AMOUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    HALF_BUTTON = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/nav/button[1]'
    DOUBLE_BUTTON = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/nav/button[2]'
    MINES_COUNT_SELECT = '//*[@id="root"]/div/aside/section/section/label/div[2]/div/div/select'
    MANUAL_TAB = '//*[@id="root"]//button[contains(text(),"Manual")]'

    # Butonlar
    PLACE_BET_BUTTON = '//*[@id="root"]/div/aside/section/section/button[1]'
    RANDOM_PICK_BUTTON = '//*[@id="root"]/div/aside/section/section/button[2]'
    COLLECT_WIN_BUTTON = '//*[@id="root"]/div/aside/section/section/button[1]'

    AUTO_TAB_BUTTON        = '//*[@id="root"]/div/aside/section/nav/button[2]'
    AUTO_BET_AMOUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    AUTO_BOMB_COUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/label/div[2]/div/div/select'
    AUTO_SPIN_COUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div/input'
    AUTO_PLAY_BUTTON       = '//*[@id="root"]/div/aside/section/section/button'

    # Oyun grid (canvas)
    GAME_BOARD_CANVAS = '//*[@id="root"]/div/div/canvas'

    DIAMONDS_INPUT = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div[2]/div/input'

    # Kazanma bildirimi
    WIN_NOTIFICATION = '//*[contains(text(), "KAZANDIN!")]'

    # **Yeni eklenen** Real/Demo play butonları:
    REAL_PLAY_BUTTON       = '//*[@id="root"]/main/div/div/div/button[1]'
    DEMO_PLAY_BUTTON       = '//*[@id="root"]/main/div/div/div/button[2]'

    # Otomatik mod bileşenleri
    AUTO_TAB_BUTTON = '//*[@id="root"]/div/aside/section/nav/button[2]'
    AUTO_BET_AMOUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    AUTO_BET_COUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div/input'
    AUTO_PLAY_BUTTON = '//*[@id="root"]/div/aside/section/section/button'







""" # locators/mines_locators.py

class MinesLocators:
    # Oyuna giriş için banner
    MINES_BANNER = '//*[@id="root"]/main/div/div[2]/div/div[2]/a[7]/img'

    # Manuel mod inputları
    BET_AMOUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    HALF_BUTTON = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/nav/button[1]'
    DOUBLE_BUTTON = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/nav/button[2]'
    MINES_COUNT_SELECT = '//*[@id="root"]/div/aside/section/section/label/div[2]/div/div/select'
    MANUAL_TAB = '//*[@id="root"]//button[contains(text(),"Manual")]'

    # Butonlar
    PLACE_BET_BUTTON = '//*[@id="root"]/div/aside/section/section/button[1]'
    RANDOM_PICK_BUTTON = '//*[@id="root"]/div/aside/section/section/button[2]'
    COLLECT_WIN_BUTTON = '//*[@id="root"]/div/aside/section/section/button[1]'

    AUTO_TAB_BUTTON        = '//*[@id="root"]/div/aside/section/nav/button[2]'
    AUTO_BET_AMOUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    AUTO_BOMB_COUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/label/div[2]/div/div/select'
    AUTO_SPIN_COUNT_INPUT  = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div/input'
    AUTO_PLAY_BUTTON       = '//*[@id="root"]/div/aside/section/section/button'

    # Oyun grid (canvas)
    GAME_BOARD_CANVAS = '//*[@id="root"]/div/div/canvas'

    DIAMONDS_INPUT = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div[2]/div/input'

    # Kazanma bildirimi
    WIN_NOTIFICATION = '//*[contains(text(), "KAZANDIN!")]'

    # **Yeni eklenen** Real/Demo play butonları:
    REAL_PLAY_BUTTON       = '//*[@id="root"]/main/div/div/div/button[1]'
    DEMO_PLAY_BUTTON       = '//*[@id="root"]/main/div/div/div/button[2]'

    # Otomatik mod bileşenleri
    AUTO_TAB_BUTTON = '//*[@id="root"]/div/aside/section/nav/button[2]'
    AUTO_BET_AMOUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[1]/div[2]/div/input'
    AUTO_BET_COUNT_INPUT = '//*[@id="root"]/div/aside/section/section/div[2]/div[2]/div/input'
    AUTO_PLAY_BUTTON = '//*[@id="root"]/div/aside/section/section/button'
 """
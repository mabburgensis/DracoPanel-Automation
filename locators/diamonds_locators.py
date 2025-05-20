# diamonds_locators.py

class DiamondsLocators:

    DIAMONDS_BANNER = '//*[@id="root"]/main/div/div[2]/div/div[2]/a[4]/img'

    # -------- Giriş & Oyun Seçim --------
    REAL_PLAY_BUTTON = '//*[@id="root"]/main/div/div/div/button[1]'
    DEMO_PLAY_BUTTON   = '//*[@id="root"]/div[2]/div/div/div/div/button[1]'   # Demo Play (eğer kullanacaksan)

    # -------- Bahis Paneli --------
    MANUAL_TAB_BUTTON      = '//*[@id="root"]/div/aside/section/nav/button[1]'
    BET_AMOUNT_INPUT       = '//*[@id="root"]/div/aside/section/section/div/div[2]/div/input'
    BET_SUBMIT_BUTTON      = '//*[@id="root"]/div/aside/section/section/button'

    # -------- Kazanç ve Oran Alanları --------
    WIN_AMOUNT_INPUT       = '//*[@id="root"]/div/div/div/div[2]/div[1]/div/input'
    MULTIPLIER_INPUT       = '//*[@id="root"]/div/div/div/div[2]/div[2]/div/input'

    # -------- Multiplier Board Satırları --------
    MULTIPLIER_50X_ROW     = '//*[@id="root"]/div/div/div/div[1]/div[1]'
    MULTIPLIER_5X_ROW      = '//*[@id="root"]/div/div/div/div[1]/div[2]'
    MULTIPLIER_4X_ROW      = '//*[@id="root"]/div/div/div/div[1]/div[3]'
    MULTIPLIER_3X_ROW      = '//*[@id="root"]/div/div/div/div[1]/div[4]'
    MULTIPLIER_2X_ROW      = '//*[@id="root"]/div/div/div/div[1]/div[5]'
    MULTIPLIER_0_10X_ROW   = '//*[@id="root"]/div/div/div/div[1]/div[6]'
    MULTIPLIER_0_00X_ROW   = '//*[@id="root"]/div/div/div/div[1]/div[7]'

    # -------- Satırlardaki Taşlar (Kutu/Elmas) --------
    # 50x satırındaki n. taş: MULTIPLIER_50X_NTH_DIAMOND.format(n)
    MULTIPLIER_50X_NTH_DIAMOND = '//*[@id="root"]/div/div/div/div[1]/div[1]/div/svg[{n}]/path'
    MULTIPLIER_5X_NTH_DIAMOND  = '//*[@id="root"]/div/div/div/div[1]/div[2]/div/svg[{n}]/path'
    MULTIPLIER_4X_NTH_DIAMOND  = '//*[@id="root"]/div/div/div/div[1]/div[3]/div/svg[{n}]/path'
    MULTIPLIER_3X_NTH_DIAMOND  = '//*[@id="root"]/div/div/div/div[1]/div[4]/div/svg[{n}]/path'
    MULTIPLIER_2X_NTH_DIAMOND  = '//*[@id="root"]/div/div/div/div[1]/div[5]/div/svg[{n}]/path'
    MULTIPLIER_0_10X_NTH_DIAMOND = '//*[@id="root"]/div/div/div/div[1]/div[6]/div/svg[{n}]/path'
    MULTIPLIER_0_00X_NTH_DIAMOND = '//*[@id="root"]/div/div/div/div[1]/div[7]/div/svg[{n}]/path'

    # NOT: Taşlar 1'den 5'e kadar (n=1..5) sıralı


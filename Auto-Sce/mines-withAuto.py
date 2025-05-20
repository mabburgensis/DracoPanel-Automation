import time, random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from common.browser_utils import open_browser, screenshot
from common.user_data import load_user_data
from locators.login_locators import LoginLocators
from locators.mines_locators import MinesLocators
from selenium.webdriver.common.keys import Keys

# Canvas’ın viewport içindeki sol-üst koordinatı ve boyutu (DevTools’dan okunan)
CANVAS_LEFT, CANVAS_TOP, CANVAS_W, CANVAS_H = 300, 0, 983, 837

# 5×5 grid’in tüm hücre merkezlerinin viewport koordinatları
CELLS = [
    {"x":398,"y":84},  {"x":595,"y":84},  {"x":792,"y":84},  {"x":988,"y":84},  {"x":1185,"y":84},
    {"x":398,"y":251},{"x":595,"y":251},{"x":792,"y":251},{"x":988,"y":251},{"x":1185,"y":251},
    {"x":398,"y":419},{"x":595,"y":419},{"x":792,"y":419},{"x":988,"y":419},{"x":1185,"y":419},
    {"x":398,"y":586},{"x":595,"y":586},{"x":792,"y":586},{"x":988,"y":586},{"x":1185,"y":586},
    {"x":398,"y":753},{"x":595,"y":753},{"x":792,"y":753},{"x":988,"y":753},{"x":1185,"y":753},
]

def switch_to_game_iframe(driver):
    """Ana sayfaya dönüp, uygun iframe’e geçer."""
    driver.switch_to.default_content()
    for iframe in driver.find_elements(By.TAG_NAME, "iframe"):
        try:
            driver.switch_to.frame(iframe)
            if driver.find_elements(By.XPATH, MinesLocators.BET_AMOUNT_INPUT):
                return True
        except:
            pass
        driver.switch_to.default_content()
    return False

def read_diamond_count(driver):
    """
    Diamonds input’unun değerini int olarak döner.
    Bulunamazsa None döner (MINE).
    """
    try:
        el = driver.find_element(By.XPATH, MinesLocators.DIAMONDS_INPUT)
        val = el.get_attribute("value") or el.get_property("value")
        return int(float(val))
    except:
        return None

def login_and_open_mines(driver, wait):
    """Giriş → Mines banner → Real Play akışını yapar."""
    print("🚀 mines.py başlatılıyor")
    driver.get("https://operator.dracofusion.com")
    time.sleep(1)

    # Login
    wait.until(EC.element_to_be_clickable((By.XPATH, LoginLocators.LOGIN_BUTTON_HEADER))).click()
    creds = load_user_data()
    wait.until(EC.visibility_of_element_located((By.XPATH, LoginLocators.USERNAME_INPUT)))\
        .send_keys(creds["username"])
    driver.find_element(By.XPATH, LoginLocators.PASSWORD_INPUT).send_keys(creds["password"])
    driver.find_element(By.XPATH, LoginLocators.SUBMIT_BUTTON).click()
    wait.until(EC.presence_of_element_located((By.XPATH, LoginLocators.LOGOUT_BUTTON)))

    # Mines banner
    print("🎮 Mines banner’a tıklanıyor...")
    banner = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_BANNER)))
    driver.execute_script("arguments[0].scrollIntoView(true);", banner)
    banner.click()
    time.sleep(1)

    # Real Play
    print("▶️ Real Play’e tıklanıyor...")
    real = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.REAL_PLAY_BUTTON)))
    real.click()
    time.sleep(3)
    screenshot(driver, "mines_game_opened")

def test_place_random_bet(driver, wait):
    """Manuel akış: random bet + bomba → Place Bet"""
    for _ in range(3):
        if switch_to_game_iframe(driver):
            break
        time.sleep(1)
    else:
        return False

    try:
        bet_in = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.BET_AMOUNT_INPUT))
        )
    except TimeoutException:
        return False

    bet_in.clear(); time.sleep(0.5)
    amt = round(random.uniform(1, 99), 2)
    bet_in.send_keys(str(amt))
    print(f"   🎲 Bet girildi: {amt}")
    time.sleep(0.5)

    mines_sel = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.MINES_COUNT_SELECT))
    )
    mines_sel.click(); time.sleep(0.5)
    idx = random.randint(1, 24)
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, f"{MinesLocators.MINES_COUNT_SELECT}/option[{idx}]"))
    ).click()
    print(f"   💣 Bomba sayısı: {idx}")
    time.sleep(0.5)

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.PLACE_BET_BUTTON))
    ).click()
    print("   ✅ Bahis gönderildi")
    screenshot(driver, "m01_bet_sent")
    time.sleep(2)
    return True

def play_until_two_diamonds(driver, wait):
    """Manuel: iki diamond üst üste açılana kadar döngü."""
    while True:
        print("\n🔄 Yeni round başlıyor…")
        if not test_place_random_bet(driver, wait):
            continue

        # Birinci pick
        driver.switch_to.default_content(); switch_to_game_iframe(driver)
        before = read_diamond_count(driver)
        try:
            pick1 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 İlk pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("▶️ İlk pick tıklanıyor…")
        pick1.click(); time.sleep(2); screenshot(driver, "after_first_pick")
        after1 = read_diamond_count(driver)
        if after1 is None or after1 >= (before or 0):
            print("💥 İlk pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("💎 İlk pick DIAMOND")

        # İkinci pick
        driver.switch_to.default_content(); switch_to_game_iframe(driver)
        before2 = after1
        try:
            pick2 = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, MinesLocators.RANDOM_PICK_BUTTON))
            )
        except TimeoutException:
            print("💥 İkinci pick butonu yok, yeniden başla")
            time.sleep(2)
            continue
        print("▶️ İkinci pick tıklanıyor…")
        pick2.click(); time.sleep(2); screenshot(driver, "after_second_pick")
        after2 = read_diamond_count(driver)
        if after2 is None or after2 >= before2:
            print("💥 İkinci pick MINE, yeniden başla")
            time.sleep(2)
            continue
        print("💎 İkinci pick DIAMOND")

        # Collect Winnings
        driver.switch_to.default_content(); switch_to_game_iframe(driver)
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, MinesLocators.COLLECT_WIN_BUTTON))
        ).click()
        print("   ✅ Collect tıklandı")
        try:
            popup = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, MinesLocators.WIN_NOTIFICATION))
            )
            print(f"   🏆 {popup.text}")
        except TimeoutException:
            print("   ⚠️ Popup yok, yine de başarılı sayılıyor")
        screenshot(driver, "final_win_collected")
        print("🎉 Manuel test tamamlandı!")
        break


def click_random_grid_cells(driver, wait, n_clicks=3):
    # 1) Canvas'ı bul
    canvas = wait.until(
        EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div/div/canvas"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", canvas)
    driver.execute_script("arguments[0].focus();", canvas)
    time.sleep(0.5)
    
    # 2) Canvas'ın boyutunu ve grid hesapla
    rect = driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {left: r.left, top: r.top, width: r.width, height: r.height};
    """, canvas)
    left, top, w, h = rect["left"], rect["top"], rect["width"], rect["height"]

    # *** Gözlemlerine göre grid, canvas'ın merkezinden başlıyor ***
    # Eğer padding/margin varsa aşağıdaki oranları ayarlayabilirsin!
    cols, rows = 5, 5
    cell_w = w / cols
    cell_h = h / rows

    # *** Seçilen hücrelerin tekrarsız olmasını sağla ***
    chosen = set()
    print(f"Canvas: {w:.0f}x{h:.0f}, Cell: {cell_w:.2f}x{cell_h:.2f}")
    for i in range(n_clicks):
        while True:
            col = random.randint(0, cols-1)
            row = random.randint(0, rows-1)
            if (row, col) not in chosen:
                chosen.add((row, col))
                break

        # Hücre merkezini hesapla (canvas koordinatı)
        offset_x = int((col + 0.5) * cell_w)
        offset_y = int((row + 0.5) * cell_h)

        # 1. Mouse'u canvas ortasına getir
        ActionChains(driver).move_to_element(canvas).perform()
        time.sleep(0.15)

        # 2. Hücre offsetine mouse ile git ve tıkla
        ActionChains(driver).move_to_element_with_offset(canvas, offset_x - w//2, offset_y - h//2).click().perform()
        time.sleep(0.10)

        # 3. JS ile click event gönder (hybrid)
        driver.execute_script("""
            const canvas = arguments[0];
            const x = arguments[1];
            const y = arguments[2];
            const evt = new MouseEvent('click', {
                bubbles: true,
                cancelable: true,
                clientX: canvas.getBoundingClientRect().left + x,
                clientY: canvas.getBoundingClientRect().top + y
            });
            canvas.dispatchEvent(evt);
        """, canvas, offset_x, offset_y)
        time.sleep(0.10)

        # 4. Canvas'a tekrar focus at
        driver.execute_script("arguments[0].focus();", canvas)
        time.sleep(0.10)

        print(f"   ✅ Hücre {i+1}: row={row}, col={col}, tıklama noktası=({offset_x},{offset_y})")

        # 5. Tıklamalar arası küçük delay
        time.sleep(0.35)

def auto_play_session(driver, wait):
    print("▶️ Manuel test bitti, Otomatik moda geçiliyor…")

    # — 1) Auto tab’e tıkla
    wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_TAB_BUTTON))).click()
    time.sleep(1)

    # — 2) Auto Bet Amount
    amt = round(random.uniform(0.1, 500.0), 2)
    bet_in = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_BET_AMOUNT_INPUT)))
    bet_in.clear(); time.sleep(0.2)
    bet_in.send_keys(str(amt))
    print(f"🎲 Auto Bet atandı: {amt}")
    time.sleep(1)

    # — 3) Number of Bets (1–10), önce Ctrl+A ile seçip üzerine yaz
    spins = random.randint(1, 10)
    spin_in = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_BET_COUNT_INPUT)))
    spin_in.click()
    time.sleep(0.2)
    spin_in.send_keys(Keys.CONTROL, 'a')   # mevcut “0”’ı seç
    spin_in.send_keys(str(spins))          # üzerine yaz
    print(f"🔄 Spin sayısı atandı: {spins}")
    time.sleep(1)

    # — 4) Auto Bomb Count
    bomb_sel = wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_BOMB_COUNT_INPUT)))
    bomb_sel.click(); time.sleep(0.5)
    bi = random.randint(1, 24)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, f"{MinesLocators.AUTO_BOMB_COUNT_INPUT}/option[{bi}]")
)).click()
    print(f"💣 Auto Bomb atandı: {bi}")
    time.sleep(1)

    # — 5) Grid hücrelerine 1–6 arası tıklama
    # iframe’e geç
    driver.switch_to.default_content()
    switch_to_game_iframe(driver)

    canvas = wait.until(EC.presence_of_element_located((By.XPATH, MinesLocators.GAME_BOARD_CANVAS)))
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", canvas)
    time.sleep(0.5)

    

    # Canvas’ın bounding rect’ini al
    rect = driver.execute_script("""
        const r = arguments[0].getBoundingClientRect();
        return {left:r.left, top:r.top, width:r.width, height:r.height};
    """, canvas)
    left, top, w, h = rect["left"], rect["top"], rect["width"], rect["height"]
    cols, rows = 5, 5
    cell_w, cell_h = w/cols, h/rows

    n_clicks = random.randint(1, 6)
    print(f"🔲 Auto: {n_clicks} kere rasgele hücre tıklanacak…")
    for i in range(n_clicks):
        col = random.randrange(cols)
        row = random.randrange(rows)
        dx = (col+0.5)*cell_w - w/2
        dy = (row+0.5)*cell_h - h/2

        ActionChains(driver) \
            .move_to_element(canvas) \
            .move_by_offset(dx, dy) \
            .click() \
            .perform()


    click_random_grid_cells(driver, wait, n_clicks=random.randint(2, 6))

    print(f"   ✅ Hücre {i+1}: row={row},col={col} → offset({int(dx)},{int(dy)})")
    time.sleep(1)

    # — 6) Auto Play başlat
    print("▶️ Otomatik bahis başlatılıyor…")
    wait.until(EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_PLAY_BUTTON))).click()

    # — 7) Spin’ler bitene kadar (buton tekrar aktifleşene dek) bekle
    WebDriverWait(driver, spins*3 + 10).until(
        EC.element_to_be_clickable((By.XPATH, MinesLocators.AUTO_PLAY_BUTTON))
    )
    print("✅ Otomatik bahis tamamlandı!")
    screenshot(driver, "auto_completed")

def test_mines_flow():
    driver, wait = open_browser()
    login_and_open_mines(driver, wait)
    play_until_two_diamonds(driver, wait)
    auto_play_session(driver, wait)
    input("\n🔵 Tüm testler bitti — Enter’a bas çık…")
    driver.quit()

if __name__ == "__main__":
    test_mines_flow()

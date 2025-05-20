# main.py
import subprocess
import os

# Test dosyalarının sıralı listesi
TEST_FILES = [
    "register.py",
    "login.py",
    "mines.py",
    "diamonds.py",
    "dice.py"
]

def run_test(file_name):
    print(f"\n🔷 Başlatılıyor: {file_name}")
    result = subprocess.run(["python", file_name])

    if result.returncode != 0:
        print(f"❌ {file_name} çalıştırılırken hata oluştu!")
        exit(1)  # Zinciri burada kes
    else:
        print(f"✅ {file_name} başarıyla tamamlandı.")

if __name__ == "__main__":
    print("=== 🧪 Otomasyon Test Başlatıcısı (main.py) ===")
    for test_file in TEST_FILES:
        print(f"DEBUG | Sıradaki dosya: {test_file}")  # <--- BURAYA EKLE
        if os.path.exists(test_file):
            print(f"DEBUG | {test_file} bulundu, run_test çağrılacak")  # <--- BURAYA EKLE
            run_test(test_file)
        else:
            print(f"⚠️ Dosya bulunamadı: {test_file}")

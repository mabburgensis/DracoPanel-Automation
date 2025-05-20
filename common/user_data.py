import json
import os

USER_DATA_FILE = "test_user_data.json"

def save_user_data(email, username, password):
    data = {
        "email": email,
        "username": username,
        "password": password
    }
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        raise FileNotFoundError("Kullanıcı verisi bulunamadı. Lütfen önce register.py çalıştırın.")
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)
import requests
import json
import os
import random
from datetime import date
from time import sleep
from flask import Flask
import threading

isLive = True
app = Flask(__name__)

@app.route('/')
def index():
    global isLive
    if isLive:
        return "Alive"
    else:
        return "Dead", 500

def randomData():
    char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(char) for _ in range(36))

url = "https://discordmanager.fly.dev"

def getData():
    global isLive
    try:
        response = requests.get(url + '/data', timeout=10)
        if response.status_code == 200:
            isLive = True
            print('PingAlive')
            return response.json()
        else:
            isLive = False
            print("Không kết nối được (status:", response.status_code, ")")
            return ''
    except Exception as e:
        isLive = False
        print("Không kết nối được:", e)
        return ''

folder = r'D:\Games\Backup'  # File name is YYYY-MM-DD.json
CAP = 20  # Max files in folder. Delete old ones.

def backup():
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Xóa file cũ nếu quá giới hạn
    files = sorted(os.listdir(folder))
    while len(files) > CAP:
        old_file = files.pop(0)
        os.remove(os.path.join(folder, old_file))
        print(f"Đã xóa: {old_file}")

    day = date.today().strftime("%Y-%m-%d")
    file_path = os.path.join(folder, f"{day}.json")

    if os.path.exists(file_path) and os.path.getsize(file_path) > 10:
        return  # Backup hợp lệ đã tồn tại

    data = getData()
    if not data:
        return  # Không có dữ liệu để backup

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Đã tạo: {file_path}")

def specialPing():
    try:
        requests.post(url + "/special", json={}, timeout=10)
        print("SpecialPing sent")
    except Exception as e:
        print("SpecialPing lỗi:", e)

def loop_task():
    while True:
        backup()
        sleep(30)
        specialPing()
        sleep(random.randint(45, 65))

def main():
    # Chạy Flask trên thread riêng
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080, debug=False), daemon=True).start()

    # Chạy vòng lặp chính
    loop_task()

if __name__ == "__main__":
    main()

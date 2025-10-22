import requests
import json
import os
import random
from datetime import date
from time import sleep
from flask import Flask, render_template_string
import threading
import asyncio

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

isLive = True

app = Flask(__name__)

@app.route('/')
def index():
    global isLive
    if isLive:
        return "Alive"
    else:
        return "Dead", 500

@app.route('/status')
def get_status():
    global isLive, url
    flyLink = url
    html = f"""
<html>
    <head><title>Status Page</title></head>
    <body>
        <p>isLive: {isLive}</p>
        <p>Fly link: <a href="{flyLink}" target="_blank">{flyLink}</a></p>
        <p>Data: <a href="{flyLink+'/data'}" target="_blank">{flyLink+'/data'}</a></p>
        <p>Logs: <a href="{flyLink+'/log'}" target="_blank">{flyLink+'/log'}</a></p>
        <p>Debug: <a href="{flyLink+'/debug'}" target="_blank">{flyLink+'/debug'}</a></p>
    </body>
</html>
""" #""""
    return render_template_string(html)

def randomData():
    char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(char) for _ in range(36))

url = "https://discordmanager.fly.dev"

def getData():
    logging.info('Start Getting Data')
    global isLive
    logging.info(str(isLive))
    try:
        response = requests.get(url + '/data', timeout=10)
        if response.status_code == 200 and len(response.text) > 100:
            isLive = True
            logging.error('Ping Server Alive')
            return response.json()
        else:
            isLive = False
            logging.error('Dead')
            return ''
    except Exception as e:
        isLive = False
        print("Không kết nối được:", e)
        logging.error('VERY DEAD')
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

async def loop_task():
    while True:
        logging.info('Start Checking')
        backup()
        await asyncio.sleep(30)
        specialPing()
        await asyncio.sleep(random.randint(45, 65))

def main():
    logging.info('Start Thread')
    threading.Thread(
        target=lambda: app.run(host='0.0.0.0', port=8080, debug=False),
        daemon=True
    ).start()

    logging.info('Start task')
    asyncio.run(loop_task())  # Chạy async event loop

if __name__ == "__main__":
    main()

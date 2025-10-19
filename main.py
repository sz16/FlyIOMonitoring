import requests
import json
import os
from datetime import date, datetime
from time import sleep
import random
from flask import Flask

app = Flask(__name__)
@app.route('/')
def index():
    return "Alive"

def randomData():
    char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(char) for i in range(36))

url = "https://discordmanager.fly.dev"
def getData():
    try:
        response = requests.get(url+'/data', timeout=10)
        if response.status_code == 200:
            print('PingAlive')
            return json.loads(response.text)
        else:
            print("Không kết nối được")
            return ''
    except Exception as e:
        print("Không kết nối được:", e)
        
folder = 'D:\\Games\\Backup' #File name is YYYY-MM-DD.json
CAP = 20 #Max file in folder. Delete old file until under CAP
def backup():
    #Check folder exist or not
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    #Delete old file
    files = sorted(os.listdir(folder))
    while len(files) > CAP:
        old_file = files.pop(0)
        os.remove(os.path.join(folder, old_file))
        print(f"Đã xóa: {old_file}")
    
    #Get current day in YYYY-MM-DD
    day = date.today().strftime("%Y-%m-%d")
    
    #Create new file
    file_path = os.path.join(folder, day + '.json')
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 10:
            #Legit backup exits
            return
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(getData(), f, ensure_ascii=False, indent=4)
    print(f"Đã tạo: {file_path}")

def specialPing():
    requests.post(url+"/special", json={})

def main():
    while True:
        backup()
        sleep(30)
        specialPing()
        sleep(random.randint(45, 65))
    
if __name__ == "__main__": main()

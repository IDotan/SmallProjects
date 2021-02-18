import socket
import subprocess
import keyboard


temp = subprocess.run('ipconfig', capture_output=True)
HOST = ''
for line in temp.stdout.decode('utf-8').split('\r'):
    if 'IPv4 Address' in line:
        HOST = line.split(':')[1].strip()
PORT = 56789
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((HOST, PORT))
while True:
    try:
        client.listen()
        connection, addr = client.accept()
        data = connection.recv(1024)
        if data == b'ThisIsACode4334':
            connection.send(b'IN')
            run = True
            while run:
                data = connection.recv(1024).decode('utf-8')
                if data == 'up':
                    keyboard.press('Volume Up')
                elif data == 'down':
                    keyboard.press('Volume Down')
                elif data == 'mute':
                    keyboard.press('volume mute')
                elif data == 'zoom':
                    subprocess.run('taskkill /im zoom.exe /f')
                elif data == 'exit':
                    run = False
        else:
            continue
    except ConnectionResetError:
        continue
    except ConnectionAbortedError:
        continue

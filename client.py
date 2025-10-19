import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

nickname = input("Masukkan nickname: ")
nim = input("Masukkan NIM: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((HOST, PORT))
    print(f"[*] Terhubung ke server di {HOST}:{PORT}")
except:
    print("Tidak dapat terhubung ke server.")
    exit()

def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            if message == 'NICK':
                client.send(nickname.encode())
            else:
                print(message)
        except:
            print("Koneksi ke server terputus.")
            client.close()
            break

def write():
    while True:
        try:
            text = input('')
            message = f"[{nim}] {nickname}: {text}"
            client.send(message.encode())
        except:
            print("Gagal mengirim pesan, koneksi putus.")
            client.close()
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

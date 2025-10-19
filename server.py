import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                client.close()
                if client in clients:
                    index = clients.index(client)
                    clients.remove(client)
                    nickname = nicknames[index]
                    nicknames.remove(nickname)
                    print(f"[DISCONNECTED] {nickname} terputus.")
                    broadcast(f"{nickname} keluar dari chat.\n".encode())

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, sender_socket=client)
        except:
            index = clients.index(client)
            client.close()
            nickname = nicknames[index]
            clients.remove(client)
            nicknames.remove(nickname)
            print(f"[DISCONNECTED] {nickname}")
            broadcast(f"{nickname} keluar dari chat.\n".encode())
            break

def receive():
    print(f"[*] Server mendengarkan di {HOST}:{PORT}")
    while True:
        client, address = server.accept()
        print(f"[*] Terhubung dengan {address}")

        client.send("NICK".encode())
        nickname = client.recv(1024).decode()
        nicknames.append(nickname)
        clients.append(client)

        print(f"[+] {nickname} bergabung ke chat")
        broadcast(f"{nickname} bergabung dalam chat!\n".encode())
        client.send("Terhubung ke server!\n".encode())

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()

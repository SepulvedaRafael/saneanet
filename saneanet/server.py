import socket

HOST = "0.0.0.0"
PORT = 7050

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print(f"Servidor aguardando conexão na porta {PORT}...")

conn, addr = servidor.accept()
print(f"Conectado por: {addr}")

with conn:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Recebido: {data.decode()}")
        conn.sendall(b"Mensagem recebida pelo servidor")

conn.close()

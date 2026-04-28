import socket

SERVER_IP = "192.168.X.X"
PORT = 5000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((SERVER_IP, PORT))

cliente.sendall(b"Ola, servidor!")

data = cliente.recv(1024)
print(f"Resposta do Servidor: {data.decode()}")

cliente.close()

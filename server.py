import socket
import pickle

host = '10.0.0.69'
port = 8912
address = (host,port)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(address)

while True:
    msg = pickle.loads(client.recv(4096))
    print(msg)

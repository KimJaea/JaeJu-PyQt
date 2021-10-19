import socket
import sys

# LOCAL: 172.24.208.1
# SERVER: 18.222.27.87
HOST = '3.16.56.48'
PORT = 8080

def return_value(data1, data2):
    print(data1 + data2)
    print('return 91')
    return '91'

print('received ' + sys.argv[1])
f = open(sys.argv[1], "r")
con = f.readlines()
f.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
for i in con:
    data = str(i)
    client_socket.send(data.encode())

data = "end"
client_socket.send(data.encode())

data = client_socket.recv(1024)
print('Received', data.decode())
# Received accuracy:0.80733429553467 loss:0.37630867958065 predict:0

client_socket.close()
datas = data.decode().split(' ')
return_value(datas[0][9:], datas[2][8])

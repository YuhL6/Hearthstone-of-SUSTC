import socket
import time
import random
def connection():
    ServerIP = '122.51.26.166'
    ServerPort = 14290
    a = 0
    time1 = time.time()
    sockets = []
    cnt = 0
    for i in range(100):
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSocket.connect(('127.0.0.1', 14290))
        ServerSocket.send(b'123\r\n\r\n')
        time.sleep(0.01)
        data = str
        data.endswith()
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect(('127.0.0.1', 14290))
        Socket.send(b'123\r\n\r\n')
        ServerSocket.send(b'111111')
        '''ServerSocket.send(b'12345')
        time.sleep(0.1)
        ServerSocket.send(b'123456')'''
        sockets.append(ServerSocket)
        print(cnt)
        cnt += 1
    time.sleep(5)
    while True:
        index = random.randint(0, 99)
        sock = sockets[index]
        print(sock)
        sock.send(b'hahaha, r u ok?')
        time.sleep(10)
        sock.send(b'hahaha?')
        cnt += 1
        print(sock.getsockname(), '        ', cnt)
        time.sleep(0.01)

if __name__ == "__main__":
    connection()
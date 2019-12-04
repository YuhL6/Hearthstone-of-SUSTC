import socket
import random
import time

user_id = 123120
password = 'mima123'

def register_test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('122.51.26.166', 14290))
    str = "200 {}\r\n".format(time.time())
    str += "{} {}\r\n{}\r\n\r\n".format(user_id, password, '{}'.format(random.random()))
    str = str.encode()
    sock.send(str)
    data = sock.recv(1024).decode()
    print(data)

def log_test():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('122.51.26.166', 14290))
    str = "210 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, password)
    str = str.encode()
    sock.send(str)
    data = sock.recv(1024).decode()
    print(data)
    time.sleep(0.1)
    sock.send(b'123123')

for i in range(100):
    user_id += 1
    log_test()
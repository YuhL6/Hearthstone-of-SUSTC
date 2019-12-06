import socket
import random
import time

user_id = 11711017
password = 'a123456'
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('122.51.26.166', 14290))

def register_test():
    str = "200 {}\r\n".format(time.time())
    str += "{} {}\r\n{}\r\n\r\n".format(user_id, password, 'Yuh')
    str = str.encode()
    sock.send(str)
    data = sock.recv(1024)
    print(data)

def log_test():
    str = "210 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, password)
    str = str.encode()
    sock.send(str)
    data = sock.recv(1024)
    print(data)


if __name__ == '__main__':
    log_test()
    while True:
        data = sock.recv(1024)
        print(data)
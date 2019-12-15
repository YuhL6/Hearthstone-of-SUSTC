import socket
import threading
import time


def register_test():
    id = input('*id: ')
    pw = input('*password: ')
    name = input('*name: ')
    email = input('email: ')
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp.connect(('122.51.26.166', 14290))
    str = "200 {}\r\n".format(time.time())
    str += "{} {}\r\n{}\r\n{}\r\n\r\n".format(id, pw, name, email)
    str = str.encode()
    tmp.send(str)
    data = tmp.recv(1024).decode()
    print(data)


def change_via_old_test():
    id = input('id: ')
    pw = input('origin password: ')
    npw = input('new password: ')
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp.connect(('122.51.26.166', 14290))
    str = '220 {}\r\n'.format(time.time())
    str += "{} {}\r\n{}\r\n\r\n".format(id, pw, npw)
    str = str.encode()
    tmp.send(str)
    data = tmp.recv(1024).decode()
    print(data)


class User:
    def __init__(self):
        self.user_id = -1
        self.room = -1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('122.51.26.166', 14290))
        self.listen = threading.Thread(target=self.listen)

    def log(self):
        id = input('id: ')
        pw = input('password: ')
        tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp.connect(('122.51.26.166', 14290))
        str = "210 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(id, pw)
        str = str.encode()
        self.sock.send(str)
        data = self.sock.recv(1024).decode().split('\r\n')
        re = data[0].split(' ')
        if re[0] != '212':
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(('122.51.26.166', 14290))
            print("Wrong password")
        else:
            self.user_id = id
            self.listen.start()

    def request(self):
        name = input("Name: ")
        str = "400 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, name)
        str = str.encode()
        self.sock.send(str)

    def accept(self):
        name = input("Name: ")
        str = "410 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, name)
        str = str.encode()
        self.sock.send(str)

    def refuse(self):
        name = input("Name: ")
        str = "415 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, name)
        str = str.encode()
        self.sock.send(str)

    def send_msg(self):
        name = input("Name: ")
        msg = input("Message: ")
        str = "420 {}\r\n".format(time.time())
        str += "{} {}\r\n{}\r\n\r\n".format(self.user_id, name, msg)
        str = str.encode()
        self.sock.send(str)

    def delete_friend(self):
        name = input("Name: ")
        str = "430 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, name)
        str = str.encode()
        self.sock.send(str)

    def list_room(self):
        str = "500 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(self.user_id)
        str = str.encode()
        self.sock.send(str)

    def create_room(self):
        str = "510 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(self.user_id)
        str = str.encode()
        self.sock.send(str)

    def add_room(self):
        room = input('room: ')
        str = "520 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, room)
        str = str.encode()
        self.sock.send(str)

    def get_ready(self):
        str = "530 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, self.room)
        str = str.encode()
        self.sock.send(str)

    def cancel_ready(self):
        str = "535 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, self.room)
        str = str.encode()
        self.sock.send(str)

    def out_room(self):
        str = "545 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(self.user_id, self.room)
        str = str.encode()
        self.sock.send(str)

    def listen(self):
        while True:
            try:
                data = self.sock.recv(1024).decode().split('\r\n')
                print('')
            except:
                time.sleep(0.5)
                continue
            re = int(data[0].split(' ')[0])
            if re == 401:
                print(data[1], data[2])
            elif re == 402:
                print("Add successfully", data[1])
            elif re == 411:
                print(data[1], data[2])
            elif re == 416:
                print(data[1], data[2])
            elif re == 421:
                print(data[1], data[2])
            elif re == 432:
                print(data[1], "is deleted")
            elif re == 433:
                print("you are deleted", data[1])
            elif re == 502:
                for i in data[1:-1]:
                    print(i)
            elif re == 511:
                print(data[1])
            elif re == 512:
                print(data[1])
                self.room = data[1]
            elif re == 521:
                print(data[1], data[2])
            elif re == 522:
                self.room = int(data[1])
            elif re == 531:
                print(data[1], data[2])
            elif re == 532:
                print("ready")
            elif re == 536:
                print(data[1], data[2])
            elif re == 537:
                print("unready")
            elif re == 546:
                print(data[1], data[2])
            elif re == 547:
                self.room = -1

            print("->", end='')
            if self.user_id != -1:
                print(self.user_id, end='->')
            if self.room != -1:
                print(self.room, end='->')

    def cmd(self):
        print("Welcome to the Hearthstone-of-SUSTC: Command-line-version\r\n"
              "// the GUI version may never come out")
        print("Now what do you want? tip: you can type 'help' or '?' to know how to use this 'GUI'")
        while True:
            print("->", end='')
            if self.user_id != -1:
                print(self.user_id, end='->')
            if self.room != -1:
                print(self.room, end='->')
            a = input()
            if a == 'help' or a == '?':
                print("0/chp:       change password via old one;\r\n"
                      "1/reg:       register;\r\n"
                      "2/log:       log;            ---if fail must restart the program\r\n"
                      "3/add:       add friend;\r\n"
                      "4/ac:        accept others' requests;\r\n"
                      "5/re:        refuse others' requests (I know you have many fans);\r\n"
                      "6/msg:       send message to your friend;\r\n"
                      "7/del:       delete your friend (careful not your girl/boyfriend);       //if you have one\r\n"
                      "8/listr:     list room;\r\n"
                      "9/create:    create room;\r\n"
                      "10/in:       add into a room;\r\n"
                      "11/ready:    get ready;\r\n"
                      "12/cancel:   cancel ready;\r\n"
                      "13/out:      get out of room;\r\n")
            elif a == '':
                pass
            elif a == '0' or a == 'chp':
                change_via_old_test()
            elif a == '1' or a == 'reg':
                register_test()
            elif a == '2' or a == 'log':
                self.log()
            elif a == '3' or a == 'add':
                self.request()
            elif a == '4' or a == 'ac':
                self.accept()
            elif a == '5' or a == 're':
                self.refuse()
            elif a == '6' or a == 'msg':
                self.send_msg()
            elif a == '7' or a == 'del':
                self.delete_friend()
            elif a == '8' or a == 'listr':
                self.list_room()
            elif a == '9' or a == 'create':
                self.create_room()
            elif a == '10' or a == 'in':
                self.add_room()
            elif a == '11' or a == 'ready':
                self.get_ready()
            elif a == '12' or a == 'cancel':
                self.cancel_ready()
            elif a == '13' or a == 'out':
                self.out_room()
            else:
                print("What the hell you are talking about, use 'help' wouldn't kill you")


if __name__ == '__main__':
    u = User()
    u.cmd()

import socket
import threading
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('122.51.26.166', 14290))


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


def log_test():
    id = input('id: ')
    pw = input('password: ')
    tmp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tmp.connect(('122.51.26.166', 14290))
    str = "210 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(id, pw)
    str = str.encode()
    sock.send(str)
    return id


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


def request(user_id):
    name = input("Name: ")
    str = "400 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, name)
    str = str.encode()
    sock.send(str)


def accept(user_id):
    name = input("Name: ")
    str = "410 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, name)
    str = str.encode()
    sock.send(str)


def refuse(user_id):
    name = input("Name: ")
    str = "415 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, name)
    str = str.encode()
    sock.send(str)


def send_msg(user_id):
    name = input("Name: ")
    msg = input("Message: ")
    str = "420 {}\r\n".format(time.time())
    str += "{} {}\r\n{}\r\n\r\n".format(user_id, name, msg)
    str = str.encode()
    sock.send(str)


def delete_friend(user_id):
    name = input("Name: ")
    str = "430 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, name)
    str = str.encode()
    sock.send(str)


def list_room(user_id):
    str = "500 {}\r\n".format(time.time())
    str += "{}\r\n\r\n".format(user_id)
    str = str.encode()
    sock.send(str)


def create_room(user_id):
    str = "510 {}\r\n".format(time.time())
    str += "{}\r\n\r\n".format(user_id)
    str = str.encode()
    sock.send(str)


def add_room(user_id):
    room = input("Room: ")
    str = "520 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, room)
    str = str.encode()
    sock.send(str)


def get_ready(user_id):
    room = input("Room: ")
    str = "530 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, room)
    str = str.encode()
    sock.send(str)


def cancel_ready(user_id):
    room = input("Room: ")
    str = "535 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, room)
    str = str.encode()
    sock.send(str)


def out_room(user_id):
    room = input("Room: ")
    str = "545 {}\r\n".format(time.time())
    str += "{} {}\r\n\r\n".format(user_id, room)
    str = str.encode()
    sock.send(str)


def listen():
    while True:
        try:
            data = sock.recv(1024).decode()
            print(data)
        except:
            time.sleep(1)


def cmd():
    global user_id
    print("Welcome to the Hearthstone-of-SUSTC: Command-line-version\r\n"
          "// the GUI version may never come out")
    print("Now what do you want? tip: you can type 'help' or '?' to know how to use this 'GUI'")
    while True:
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
                  "10/inroom:   add into a room;\r\n"
                  "11/ready:    get ready;\r\n"
                  "12/cancel:   cancel ready;\r\n"
                  "13/outroom:  get out of room;\r\n")
        elif a == '':
            pass
        elif a == '0' or a == 'chp':
            change_via_old_test()
        elif a == '1' or a == 'reg':
            register_test()
        elif a == '2' or a == 'log':
            user_id = log_test()
        elif a == '3' or a == 'add':
            request(user_id)
        elif a == '4' or a == 'ac':
            accept(user_id)
        elif a == '5' or a == 're':
            refuse(user_id)
        elif a == '6' or a == 'msg':
            send_msg(user_id)
        elif a == '7' or a == 'del':
            delete_friend(user_id)
        elif a == '8' or a == 'listr':
            list_room(user_id)
        elif a == '9' or a == 'create':
            create_room(user_id)
        elif a == '10' or a == 'inroom':
            add_room(user_id)
        elif a == '11' or a == 'ready':
            get_ready(user_id)
        elif a == '12' or a == 'cancel':
            cancel_ready(user_id)
        elif a == '13' or a == 'outroom':
            out_room(user_id)
        else:
            print("What the hell you are talking about, use 'help' wouldn't kill you")


if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=cmd)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

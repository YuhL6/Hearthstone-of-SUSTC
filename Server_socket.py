import asyncio
import time
import random
import os
import urllib
import mimetypes
#import MySQLdb

#database = MySQLdb.connect("localhost", "root", "123456", "ooad_proj", charset='utf8')
#cursor = database.cursor()
ServerPort = 12345
User_count = 0
users = {}
'''class User():
    def __init__(self):
        self.pos
        self.addr
        self.last_time
        self.id
        self.mes = []

class Resolver:
    def __init__(self, data=[]):
        self.method = int(data[0].split(' ')[0])
        self.time_stamp = int(data[0].split(' ')[1])
        self.resolve(data)
        self.id = self.data[1].split(' ')[0]

    def resolve(self, data):
        if self.method == 200:
            return self.register()
        elif self.method == 210:
            return self.recognition()
        elif self.method == 220:
            self.method = 220
            self.change_password_via_old()
        elif self.method == 230 or self.method == 240 or self.method == 300 or self.method == 305 or self.method == 310 or self.method == 315:
            pass
        elif self.method == 320:
            self.method = 320
        elif self.method == '330':
            self.method = 330
        elif self.method == '340':
            self.method = 340
        elif self.method == '350':
            self.method = 350
        elif method == '360':
            self.method = 360
        elif method == '370':
            self.method = 370
        elif method == '380':
            self.method = 380
        elif method == '390':
            self.method = 390
        elif method == '395':
            self.method = 395
        elif method == '400':
            self.method = 400
        elif method == '410':
            self.method = 410
        elif method == '420':
            self.method = 420
        elif method == '430':
            self.method = 430
        elif method == '500':
            self.method = 500
        elif method == '510':
            self.method = 510
        elif method == '520':
            self.method = 520
        elif method == '530':
            self.method = 530
        elif method == '540':
            self.method = 540

    def register(self, data):
        password = data[1].split(' ')[1]
        self.name = data[2]
        return password

    def recognition(self, data):
        password = data[1].split(' ')[1]
        return password
    def change_password_via_old(self, data):
        password = (data[1].split(' ')[1], data[2])
        return password

    def packet(self, data):
        self.list_name = data[1].split(' ')[1]

    def addCardToPacket(self, data):
        self.list_name = data[1].split(' ')[1]
        for i in range()'''

async def listener(reader, writer):
    addr = writer.get_extra_info('peername')
    data = []
    while True:
        temp = await reader.readline()
        temp.decode()
        print(temp)
        print(addr)
        print(time.time())
        data.append(temp)
        if temp == b'':
            break
    # mes = Executor(data)
    # writer.write(mes)
    await writer.drain()
    writer.close()
    print(2)
async def do():
    await asyncio.gather(a(), a(), a())
async def a():
    x = random.random()
    if x > 0.2:
        print('a')
        await asyncio.sleep(1)
    else:
        time.sleep(1)
    print('b')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(listener, '', 8080, loop=loop)
    tasks = asyncio.gather(asyncio.wait((coro, a)))
    server = loop.run_until_complete(tasks)
    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


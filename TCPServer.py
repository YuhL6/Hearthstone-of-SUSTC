import selectors
import socket
import time
import Conn_to_database
import Games

ServerPort = 14290
users = {}
rooms = {}


class Resolver:
    def __init__(self):
        self.id = None
        self.time = None
        self.method = None
        self.email = ''

    def resolve(self, data: list):
        self.id = int(data[1].split(' ')[0])
        self.time = int(data[0].split(' ')[1])
        self.method = int(data[0].split(' ')[0])
        if self.method == 200:
            self.password = data[1].split(' ')[1]
            self.user_name = data[2]
            if len(data) >= 4:
                self.email = data[3]
        elif self.method == 210:
            self.password = data[1].split(' ')[1]
        elif self.method == 220:
            self.old_password = data[1].split(' ')[1]
            self.new_password = data[2]
        elif self.method == 315 or self.method == 320 or self.method == 325 or self.method == 330:
            self.list_name = data[1].split(' ')[1]
        elif self.method == 340:
            self.list_name = data[1].split(' ')[1]
            self.card_num = int(data[2])
        elif self.method == 370:
            self.room_num = int(data[1].split(' ')[1])
        elif self.method == 400:
            self.receiver = data[1].split(' ')[1]
        elif self.method == 410:
            self.sender = data[1].split(' ')[1]
        elif self.method == 420:
            self.receiver = data[1].split(' ')[1]
            self.message = data[2]
        elif self.method == 430:
            self.delete_name = data[1].split(' ')[1]
        elif self.method == 500 or self.method == 510 or self.method == 520 or self.method == 530 or self.method == 540:
            self.room_num = int(data[1].split(' ')[1])
        elif self.method == 550:
            self.room_num = int(data[1].split(' ')[1])
            self.message = data[2]


class Generator:
    def __init__(self):
        pass

    def register_refuse(self, reason):
        str = '201 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str

    def register_success(self):
        str = '202 {}\r\n'.format(time.time())
        str += '\r\n'
        return str

    def log_refuse(self, reason):
        str = '211 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str

    def log_success(self, li: list):
        st = '212 {}\r\n'.format(time.time())
        for e in li:
            st += str(e)
            st += '\r\n'
        st += '\r\n'
        return st


class Executor:
    def __init__(self):
        self.resolver = Resolver()
        self.generator = Generator()
        self.conn_db = Conn_to_database.Conn_DB()

    def execute(self, data):
        self.resolver.resolve(data)
        print(self.resolver.method)
        if self.resolver.method == 200:
            return self.register()
        elif self.resolver.method == 210:
            self.log()

    def register(self):
        print('registering')
        res = self.conn_db.register(self.resolver.id, self.resolver.password, self.resolver.user_name,
                                    self.resolver.email)
        print('res: ', res)
        if res == 0:
            # successfully register
            return self.generator.register_success()
        elif res == -1:
            return self.generator.register_refuse('user id already exists')
        elif res == -2:
            return self.generator.register_refuse('user name already exists')
        else:
            return self.generator.register_refuse('email already exists')

    def log(self):
        res = self.conn_db.log(self.resolver.id, self.resolver.password)
        if res == 0:
            return self.generator.log_refuse('user id not exists')
        elif res == 1:
            return self.generator.log_refuse('Wrong password')
        else:
            li = []
            return self.generator.log_success(li)


class TCPServer:
    def __init__(self):
        self.sel = selectors.DefaultSelector()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server is on")
        self.executor = Executor()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        data = conn.recv(1024)
        data = data.decode()
        if data:
            if not data.endswith('\r\n'):
                print(1)
                return -1
            data = data.split('\r\n')
            if len(data) < 2:
                print(2)
                return -2
            ctime = int(data[0].split(' ')[1])
            if time.time() - ctime > 3.5:
                print(ctime)
                print(time.time())
                print(3)
                return -3
            try:
                print(data)
                msg = self.executor.execute(data)
                print('msg: ', msg)
                msg = msg.encode()
                conn.send(msg)
                print('done')
            except:
                return -4
        else:
            print('closing', conn)
            self.sel.unregister(conn)
            conn.close()

    def send(self, id, msg):
        User = users[id]
        sock = User.socket
        sock.send(msg)

    def broadcast(self, li: list, msg):
        for i in li:
            self.send(i, msg)

    def start_server(self):
        self.sock.bind(('', 14290))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)


if __name__ == '__main__':
    server = TCPServer()
    server.start_server()

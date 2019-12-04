import selectors
import socket
import time
import Conn_to_database
import Games

ServerPort = 14290
users = {}
rooms = {}
undetermined_list = {}
sel = selectors.DefaultSelector()


class Resolver:
    def __init__(self):
        self.data = None
        self._id = None
        self._time = None
        self._method = None

    def resolve(self, data: list):
        self.data = data
        self._id = data[1].split(' ')[0]
        self._time = float(data[0].split(' ')[1])
        self._method = int(data[0].split(' ')[0])

    def get_id(self):
        return self._id

    def get_method(self):
        return self._method

    def get_time(self):
        return self._time

    def get_password(self):
        try:
            return self.data[1].split(' ')[1]
        except:
            return None

    def get_user_name(self):
        try:
            return self.data[2]
        except:
            return None

    def get_email(self):
        try:
            email = self.data[3]
            if email != '':
                return email
            else:
                return None
        except:
            return None

    def get_new_password(self):
        try:
            return self.data[2]
        except:
            return None

    def get_list_name(self):
        try:
            return self.data[1].split(' ')[1]
        except:
            return None

    def get_card_name(self):
        try:
            return int(self.data[2])
        except:
            return None

    def get_room_num(self):
        try:
            return int(self.data[1].split(' ')[1])
        except:
            return None

    def get_receiver(self):
        try:
            return self.data[1].split(' ')[1]
        except:
            return None

    def get_sender(self):
        try:
            return self.data[1].split(' ')[1]
        except:
            return None

    def get_delete_num(self):
        try:
            return self.data[1].split(' ')[1]
        except:
            return None

    def get_room_num(self):
        try:
            return int(self.data[1].split(' ')[1])
        except:
            return None

    def get_message(self):
        try:
            return self.data[2]
        except:
            return None


class Generator:
    def __init__(self):
        pass

    def register_refuse(self, reason):
        str = '201 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str.encode()

    def register_success(self):
        str = '202 {}\r\n'.format(time.time())
        str += '\r\n'
        return str.encode()

    def log_refuse(self, reason):
        str = '211 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str.encode()

    def log_success(self, li: list):
        st = '212 {}\r\n'.format(time.time())
        for e in li:
            st += str(e)
            st += '\r\n'
        st += '\r\n'
        print('st: ', st)
        return st.encode()

    def change_pass_suc(self):
        str = '222 {}\r\n'.format(time.time())
        str += '\r\n'
        return str.encode()

    def change_pass_fail(self, reason):
        str = '221{}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str.encode()

    def request(self, name):
        str = '400 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        return str.encode()

    def request_accept(self):
        str = '402 {}\r\n'.format(time.time())


class Executor:
    def __init__(self):
        self.resolver = Resolver()
        self.generator = Generator()
        self.conn_db = Conn_to_database.Conn_DB()

    def execute(self, data, conn):
        self.resolver.resolve(data)
        if self.resolver.get_method() == 200:
            msg = self.register()
            conn.send(msg)
            sel.unregister(conn)
            conn.close()
        elif self.resolver.get_method() == 210:
            self.log(conn)
        elif self.resolver.get_method() == 220:
            self.change_via_old(conn)
        else:
            try:
                users[self.resolver.get_id()]
            except:
                conn.send('Invalid access, please re-login')
                sel.unregister(conn)
                conn.close()

    def register(self):
        """in this function, user_id is integer"""
        res = self.conn_db.register(int(self.resolver.get_id()), self.resolver.get_password()
                                    , self.resolver.get_user_name(), self.resolver.get_email())
        if res == 0:
            # successfully register
            return self.generator.register_success()
        elif res == -1:
            return self.generator.register_refuse('user id already exists')
        elif res == -2:
            return self.generator.register_refuse('user name already exists')
        else:
            return self.generator.register_refuse('email already exists')

    def log(self, conn):
        """in this function, user_id is integer"""
        res = self.conn_db.log(int(self.resolver.get_id()), self.resolver.get_password())
        if res == -1:
            conn.send(self.generator.log_refuse('user id not exists'))
            sel.unregister(conn)
            conn.close()
        elif res == -2:
            conn.send(self.generator.log_refuse('Wrong password'))
            sel.unregister(conn)
            conn.close()
        else:
            li = self.conn_db.get_user_info(self.resolver.get_id())
            print("li: ", li)
            res = self.conn_db.get_friend_list(int(self.resolver.get_id()))
            print("res: ", res)
            player = Games.Player(self.resolver.get_id(), conn, self.resolver.get_time(), li, res)
            users[player.get_name()] = player
            try:
                un = undetermined_list[player.get_name()]
                print("un: ", un)
            except:
                pass
            info = li
            print("info: ", info)
            conn.send(self.generator.log_success(li))

    def change_via_old(self, conn):
        """in this function, user_id is integer"""
        res = self.conn_db.log(int(self.resolver.get_id()), self.resolver.get_password())
        if res == -1:
            conn.send(self.generator.change_pass_fail('user id not exists'))
            sel.unregister(conn)
            conn.close()
        elif res == -2:
            conn.send(self.generator.change_pass_fail('Wrong password'))
            sel.unregister(conn)
            conn.close()
        else:
            self.conn_db.change_password(self.resolver.get_id(), self.resolver.get_new_password())
            conn.send(self.generator.change_pass_suc())
            sel.unregister(conn)
            conn.close()

    def request_relation(self):
        """in this condition, once a player send one request message, undetermined_list would check the message exists
        or not, if not, documents the message, else ignores it, after another side responses to the request, the
        undetermined_list would add the message into the database and then delete it"""
        sender = self.resolver.get_id()
        receiver = self.resolver.get_receiver()
        try:
            un = undetermined_list[receiver]
            # if the the request is frequent, no action 
            if self.resolver.get_time() - un[sender] < 3:
                return
            un[sender] = self.resolver.get_time()
        except:
            undetermined_list[receiver] = {sender: self.resolver.get_time()}

        users[receiver].socket.send(self.generator.request(sender))

    def accept_relation(self, conn):
        sender = self.resolver.get_sender()
        try:
            del undetermined_list[self.resolver.get_id()][sender]
            users[self.resolver.get_id()].conn.send()
            users[sender].conn.send()
            self.conn_db.add_relation()
        except:
            conn.send(b'No request')

    def refuse_relation(self, conn):
        sender = self.resolver.get_sender()
        try:
            del undetermined_list[self.resolver.get_id()][sender]
            users[self.resolver.get_id()].conn.send()
            users[sender].conn.send()
        except:
            conn.send(b'No request')

class TCPServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server is on")
        self.executor = Executor()
        self.start_server()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        """cause the conn is not blocking, so try to get the recv_message, if the data does not obey the form or the
        time exceed the limitation, the conn will be rejected"""
        try:
            data = conn.recv(1024)
        except:
            sel.unregister(conn)
            conn.close()
            return -1

        data = data.decode()

        if data:
            if not data.endswith('\r\n\r\n'):
                conn.send(b'Invalid message')
                sel.unregister(conn)
                conn.close()
                return -2

            data = data.split('\r\n')

            if len(data) < 2:
                conn.send(b'Invalid message')
                sel.unregister(conn)
                conn.close()
                return -2

            ctime = float(data[0].split(' ')[1])

            if time.time() - ctime > 3.5:
                conn.send(b'Time exceed')
                sel.unregister(conn)
                conn.close()
                return -3
            try:
                print("connection accepted")
                print(data)
                self.executor.execute(data, conn)
            except:
                sel.unregister(conn)
                conn.close()
                return -4
        else:
            conn.send(b'Invalid message')
            print('closing', conn)
            sel.unregister(conn)
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
        sel.register(self.sock, selectors.EVENT_READ, self.accept)


def run():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    server = TCPServer()
    run()

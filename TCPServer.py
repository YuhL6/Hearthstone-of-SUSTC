import selectors
import socket
import heapq
import random
import time
import Conn_to_database
import Games
from Tools import *

ServerPort = 14290
# names: user_name -> user_id
names = {}
# users: user_id -> conn
users = {}
# socks: conn -> users
socks = {}
rooms = {}
cards = {}
undetermined_list = {}
sel = selectors.DefaultSelector()
conn_db = Conn_to_database.Conn_DB()
available_ids = []


class Executor:
    def __init__(self):
        self.resolver = Resolver()
        self.generator = Generator()

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
            '''avoid invalid information'''
            try:
                # one logs tries to operates other account
                if socks[conn].get_id() != self.resolver.get_id():
                    conn.send(b'Invalid access, please re-login')
                    sel.unregister(conn)
                    conn.close()
                    return
            except:
                # one un-log wants to do sth.
                conn.send(b'Invalid access, please login')
                sel.unregister(conn)
                conn.close()
                return
        if self.resolver.get_method() == 400:
            self.request_relation(conn)
        elif self.resolver.get_method() == 410:
            self.accept_relation(conn)
        elif self.resolver.get_method() == 415:
            self.refuse_relation(conn)
        elif self.resolver.get_method() == 420:
            self.chat_with(conn)
        elif self.resolver.get_method() == 430:
            self.delete_relation(conn)
        elif self.resolver.get_method() == 500:
            self.list_room(conn)
        elif self.resolver.get_method() == 510:
            self.create_room(conn)
        elif self.resolver.get_method() == 520:
            self.add_into_room(conn)
        elif self.resolver.get_method() == 530:
            self.get_ready(conn)
        elif self.resolver.get_method() == 535:
            self.cancel_ready(conn)
        elif self.resolver.get_method() == 545:
            self.leave_room(conn)
        elif self.resolver.get_method() == 550:
            self.start(conn)
        elif self.resolver.get_method() == 570:
            self.chat_in_room()
        elif self.resolver.get_method() == 580:
            self.put_card(conn)
        elif self.resolver.get_method() == 590:
            self.attack(conn)
        elif self.resolver.get_method() == 600:
            self.round_end(conn)

    def register(self):
        """in this function, user_id is integer"""
        res = conn_db.register(int(self.resolver.get_id()), self.resolver.get_password()
                               , self.resolver.get_user_name(), self.resolver.get_email())
        if res == 0:
            # successfully register
            names[self.resolver.get_user_name()] = self.resolver.get_id()
            return self.generator.register_success()
        elif res == -1:
            return self.generator.register_refuse('user id already exists')
        elif res == -2:
            return self.generator.register_refuse('user name already exists')
        else:
            return self.generator.register_refuse('email already exists')

    def log(self, conn):
        """in this function, user_id is integer!
        first we check the basic information, then we determine whether this user has been logged or not,
        if yes, out the former
        return the basic information, if the user is in game(reconnect), return the room information"""
        res = conn_db.log(int(self.resolver.get_id()), self.resolver.get_password())
        if res == -1:
            conn.send(self.generator.log_refuse('user id not exists'))
            sel.unregister(conn)
            conn.close()
        elif res == -2:
            conn.send(self.generator.log_refuse('Wrong password'))
            sel.unregister(conn)
            conn.close()
        else:
            user_info = conn_db.get_user_info(self.resolver.get_id())
            # the first element of user_info is the total game number, the second is the rate
            print("info: ", user_info)
            fr_li = conn_db.get_friend_list(int(self.resolver.get_id()))
            print("friends: ", fr_li)
            # multi-log covers
            player = Games.Player(self.resolver.get_id(), conn, self.resolver.get_time(), user_info[0], fr_li)
            for i in fr_li:
                if fr_li[i][1] == 1:
                    try:
                        users[names[i]].send(self.generator.friend_online(player.get_name()))
                        socks[users[names[i]]].friend_online(player.get_name())
                    except:
                        # means user i log out
                        pass
            try:
                u = users[self.resolver.get_id()]
                if u != conn:
                    u.send(b'another one is using this account')
                    socks[conn] = socks[u]
                    users[self.resolver.get_id()] = conn
                    sel.unregister(u)
                    u.close()
                    del socks[u]
            except:
                users[self.resolver.get_id()] = conn
                socks[conn] = player
            try:
                un = undetermined_list[self.resolver.get_id()]
                print("un: ", un)
            except:
                un = []
            conn.send(self.generator.log_success(user_info, fr_li, un))

    def change_via_old(self, conn):
        """in this function, user_id is integer"""
        res = conn_db.log(int(self.resolver.get_id()), self.resolver.get_password())
        if res == -1:
            conn.send(self.generator.change_pass_fail('user id not exists'))
            sel.unregister(conn)
            conn.close()
        elif res == -2:
            conn.send(self.generator.change_pass_fail('Wrong password'))
            sel.unregister(conn)
            conn.close()
        else:
            conn_db.change_password(self.resolver.get_id(), self.resolver.get_new_password())
            conn.send(self.generator.change_pass_suc())
            sel.unregister(conn)
            conn.close()
            try:
                conn = users[self.resolver.get_id()]
                conn.send(self.generator.wrong_access("Password has been changed, please re-login"))
                del users[self.resolver.get_id()]
                del socks[conn]
                sel.unregister(conn)
                conn.close()
            except:
                pass

    def request_relation(self, conn):
        """in this condition, once a player send one request message, undetermined_list would check the message exists
        or not, if not, documents the message, else ignores it, after another side responses to the request, the
        undetermined_list would add the message into the database and then delete it"""

        if self.resolver.get_receiver() == socks[conn].get_name():
            conn.send(self.generator.request_fail(self.resolver.get_receiver(), "Lonely kid"))
            return -1
        try:
            if len(socks[conn].get_friend_list()[self.resolver.get_receiver()]) != 0:
                conn.send(self.generator.request_fail(self.resolver.get_receiver(), "Already your friend"))
            return
        except:
            pass

        try:
            receiver = names[self.resolver.get_receiver()]
        except:
            receiver: str = self.resolver.get_receiver()
            if not receiver.isdigit():
                conn.send(self.generator.request_fail(self.resolver.get_receiver(), "No such user exists"))
                return
            if not conn_db.check_duplicate('user_info', 'user_id', 'user_id = {}'.format(receiver)):
                conn.send(self.generator.request_fail(self.resolver.get_receiver(), "No such user exists"))
                return
        try:
            un = undetermined_list[receiver]
        except:
            undetermined_list[receiver] = {}
        undetermined_list[receiver][socks[conn].get_name()] = 1
        try:
            users[receiver].send(self.generator.request(socks[conn].get_name()))
        except:
            pass

    def accept_relation(self, conn):
        sender = self.resolver.get_sender()
        receiver = self.resolver.get_id()
        try:
            del undetermined_list[receiver][sender]
            try:
                users[names[sender]].send(self.generator.add_success(socks[conn].get_name(), 1))
                conn.send(self.generator.add_success(self.resolver.get_sender(), 1))
            except:
                conn.send(self.generator.add_success(self.resolver.get_sender(), 0))
            try:
                socks[conn].add_friend(sender)
                socks[users[names[sender]]].add_friend(socks[conn].get_name())
            except:
                pass
            conn_db.add_relation(names[sender], receiver)
        except:
            conn.send(self.generator.accept_fail(sender, "No request"))

    def refuse_relation(self, conn):
        sender = self.resolver.get_sender()
        receiver = self.resolver.get_id()
        try:
            del undetermined_list[receiver][sender]
            try:
                users[names[sender]].send(self.generator.request_fail(socks[conn].get_name(), "The user refused you"
                                                                                              "r request"))
            except:
                pass
        except:
            conn.send(b'No request')

    def delete_relation(self, conn):
        id1 = self.resolver.get_id()
        id2 = names[self.resolver.get_delete_name()]
        try:
            socks[conn].delete_friend(self.resolver.get_delete_name())
            socks[users[id2]].delete_friend(socks[conn].get_name())
        except:
            pass
        if conn_db.delete_relation(id1, id2):
            try:
                users[id2].send(self.generator.deleted(socks[conn].get_name()))
            except:
                pass
            conn.send(self.generator.delete_success(self.resolver.get_delete_name()))
        else:
            conn.send(self.generator.delete_fail(self.resolver.get_delete_name(), "The user is not your friend or not "
                                                                                  "exists"))

    def chat_with(self, conn):
        """receiver can only be name"""
        global receiver
        try:
            receiver = names[self.resolver.get_receiver()]
        except:
            conn.send(self.generator.send_msg_fail(receiver, 'User not exists'))
            return
        try:
            users[receiver].send(self.generator.send_msg(socks[conn].get_name(), self.resolver.get_message()))
        except:
            conn.send(self.generator.send_msg_fail(receiver, 'User not online'))

    def list_room(self, conn):
        conn.send(self.generator.list_room(rooms))

    def create_room(self, conn):
        if socks[conn].get_status() > 1:
            conn.send(self.generator.create_room_fail("Status error"))
            return
        if len(available_ids) == 0:
            new_id = len(rooms) + 1
        else:
            new_id = heapq.heappop(available_ids)
        room = Games.Room(new_id, self.resolver.get_id(), socks[conn].get_name())  # no password version
        rooms[new_id] = room
        socks[conn].in_room(new_id)
        socks[conn].ready()
        # user status changes, need broadcast
        conn.send(self.generator.create_room_suc(new_id))
        fr_li = socks[conn].get_friend_list()
        for i in fr_li:
            if fr_li[i][1] == 1:
                try:
                    socks[users[names[i]]].friend_in_room(socks[conn].get_name())
                    users[names[i]].send(self.generator.friend_in_room(socks[conn].get_name()))
                except:
                    pass
        # room list changes, need broadcast
        for user in users:
            try:
                users[user].send(self.generator.new_room(new_id, socks[conn].get_name()))
            except:
                # user outline
                pass

    def add_into_room(self, conn):
        room_id = self.resolver.get_room_num()
        try:
            room = rooms[room_id]
        except:
            conn.send(self.generator.add_room_fail(room_id, "No room exists"))
            return
        res = socks[conn].in_room(room_id)
        if res == -1:
            conn.send(self.generator.add_room_fail(room_id, "Status error"))
            return
        res = room.add_player(self.resolver.get_id(), socks[conn].get_name())
        if res == -1:
            socks[conn].out_room()
            conn.send(self.generator.add_room_fail(room_id, "Wrong password"))
        elif res == -2:
            socks[conn].out_room()
            conn.send(self.generator.add_room_fail(room_id, "The room is full"))
        else:
            conn.send(self.generator.add_room_suc(room_id, room.get_owner_name()))
            try:
                users[room.get_owner()].send(self.generator.player_in(room_id, socks[conn].get_name()))
            except:
                # owner is outline
                pass
            fr_li = socks[conn].get_friend_list()
            for i in fr_li:
                if fr_li[i][1] == 1:
                    try:
                        users[names[i]].send(self.generator.friend_in_room(socks[conn].get_name()))
                        socks[users[names[i]]].friend_in_room(socks[conn].get_name())
                    except:
                        pass
            for user in users:
                try:
                    users[user].send(self.generator.room_full(self.resolver.get_room_num()))
                except:
                    pass

    def get_ready(self, conn):
        if socks[conn].get_room() != self.resolver.get_room_num():
            conn.send(self.generator.ready_fail(self.resolver.get_room_num(), "You are ont in the room"))
            return
        room_id = self.resolver.get_room_num()
        room = rooms[room_id]
        res = socks[conn].ready()
        if res == -1:
            conn.send(self.generator.ready_fail(room_id, "Status error: user"))
            return
        res = room.ready()
        if res == -1:
            socks[conn].not_ready()
            conn.send(self.generator.ready_fail(room_id, "Status error: room"))
            return
        conn.send(self.generator.ready_suc(room_id))
        try:
            users[room.get_owner()].send(self.generator.player_ready(room_id))
        except:
            pass

    def cancel_ready(self, conn):
        if socks[conn].get_room() != self.resolver.get_room_num():
            conn.send(self.generator.ready_fail(self.resolver.get_room_num(), "You are not in the room"))
            return
        if socks[conn].get_id() == rooms[socks[conn].get_room()].get_owner():
            conn.send(self.generator.ready_fail(self.resolver.get_room_num(), "Owner cannot cancel ready"))
            return
        res = socks[conn].not_ready()
        if res == -1:
            conn.send(self.generator.ready_fail(self.resolver.get_room_num(), "Status error: user"))
            return
        res = rooms[self.resolver.get_room_num()].not_ready()
        if res == -1:
            socks[conn].ready()
            conn.send(self.generator.ready_fail(self.resolver.get_room_num(), "Status error: room"))
            return
        conn.send(self.generator.cancel_ready_suc(self.resolver.get_room_num()))
        try:
            users[rooms[self.resolver.get_room_num()].get_owner()].send(self.generator.player_not_ready(
                self.resolver.get_room_num()))
        except:
            pass

    def leave_room(self, conn):
        global msg
        room_id = int(self.resolver.get_room_num())
        if socks[conn].get_room() != room_id:
            conn.send(self.generator.leave_room_fail(room_id, "You are not in the room"))
            return
        room = rooms[room_id]
        res = socks[conn].out_room()
        if res == -1:
            conn.send(self.generator.leave_room_fail(room_id, "Status error: user"))
            return
        res = room.delete_player(self.resolver.get_id())
        if res == -1:
            socks[conn].in_room(room_id)
            conn.send(self.generator.leave_room_fail(room_id, "Room is gaming"))
            return
        elif res == -2:
            socks[conn].in_room(room_id)
            conn.send(self.generator.leave_room_fail(room_id, "Invalid operation"))
            return
        elif res == 0:
            conn.send(self.generator.leave_room_suc(room_id))
            msg = self.generator.room_empty(room_id)
            try:
                users[room.get_owner()].send(self.generator.player_out(room_id))
            except:
                # owner is outline
                pass
        elif res == 1:
            socks[users[room.get_owner()]].ready()
            conn.send(self.generator.leave_room_suc(room_id))
            msg = self.generator.owner_change(room_id, room.get_owner_name())
        elif res == 2:
            conn.send(self.generator.leave_room_suc(self.resolver.get_room_num()))
            msg = self.generator.delete_room(self.resolver.get_room_num())
            heapq.heappush(available_ids, self.resolver.get_room_num())
            del rooms[room_id]
        fr_li = socks[conn].get_friend_list()
        for i in fr_li:
            if fr_li[i][1] == 1:
                try:
                    socks[users[names[i]]].friend_out_room(socks[conn].get_name())
                    users[names[i]].send(self.generator.friend_out_room(socks[conn].get_name()))
                except:
                    pass
        # room list changes, need broadcast
        for user in users:
            try:
                users[user].send(msg)
            except:
                # user outline
                pass

    def start(self, conn):
        room_id = int(self.resolver.get_room_num())
        room: Games.Room = rooms[room_id]
        print(socks[conn].get_status())
        if room.get_owner() != self.resolver.get_id():
            '''owner operates only'''
            conn.send(b'invalid operation')
            return
        res = socks[conn].start()
        if res == -1:
            '''you are not ready'''
            conn.send(b"Wrong0")
            return
        try:
            res = socks[users[room.get_attacker()]].start()
            if res == -1:
                '''another one not ready'''
                socks[conn].undo_start()
                conn.send(b"Wrong1")
                return
        except:
            socks[conn].undo_start()
            conn.send(b'no player')
            return
        res = room.start_game(self.resolver.get_time())
        if res == -1:
            '''room not ready'''
            socks[conn].undo_start()
            socks[users[room.get_attacker()]].undo_start()
            conn.send(b"Wrong2")
            return
        fr_li = socks[conn].get_friend_list()
        for i in fr_li:
            if fr_li[i][1] == 1:
                try:
                    socks[users[names[i]]].friend_out_room(socks[conn].get_name())
                    users[names[i]].send(self.generator.friend_out_room(socks[conn].get_name()))
                except:
                    pass
        fr_li = socks[users[room.get_attacker()]].get_friend_list()
        for i in fr_li:
            if fr_li[i][1] == 1:
                try:
                    socks[users[names[i]]].friend_out_room(socks[conn].get_name())
                    users[names[i]].send(self.generator.friend_out_room(socks[conn].get_name()))
                except:
                    pass
        li = random.sample(range(1, len(cards)), 15)
        di = {}
        for i in li:
            di[i] = cards[i]
        if random.random() > 0.5:  # get the priority
            id0 = self.resolver.get_id()
            id1 = room.get_attacker()
            conn.send(self.generator.start_game_suc(room_id, 0, li))
        else:
            id0 = room.get_attacker()
            id1 = self.resolver.get_id()
            users[id0].send(self.generator.start_game_suc(room_id, 0, li))
        room.field.set_first(id0, li, di)
        li = random.sample(range(1, len(cards)), 15)
        users[id1].send(self.generator.start_game_suc(room_id, 1, li))
        di = {}
        for i in li:
            di[i] = cards[i]
        room.field.set_last(id1, li, di)

    def chat_in_room(self):
        room_id = self.resolver.get_room_num()
        room = rooms[room_id]
        if self.resolver.get_id() == room.get_owner:
            id = room.get_attacker()
        else:
            id = room.get_owner()
        users[id].send(self.generator.msg_in_room(room_id, self.resolver.get_message()))

    def put_card(self, conn):
        room_id = self.resolver.get_room_num()
        room = rooms[room_id]
        if room.get_status() != 3:
            conn.send(b"Invalid operation")
            return
        res = room.field.put_card(self.resolver.get_id(), self.resolver.get_card())
        if res == -1:
            conn.send(b'Not your turn')
            return
        elif res == -2:
            conn.send(b'Not in your cards')
            return
        elif res == -3:
            conn.send(b'already exists')
            return
        if self.resolver.get_id() == room.get_attacker():
            users[room.get_owner()].send(self.generator.put_card_suc(self.resolver.get_card()))
        elif self.resolver.get_id() == room.get_owner():
            users[room.get_attacker()].send(self.generator.put_card_suc(self.resolver.get_card()))

    def attack(self, conn):
        room_id = self.resolver.get_room_num()
        room = rooms[room_id]
        if self.resolver.get_id() == room.get_attacker():
            id = room.get_owner()
        elif self.resolver.get_id() == room.get_owner():
            id = room.get_attacker()
        else:
            conn.send(b'Invalid operation')
            return
        if room.get_status() != 3:
            conn.send(b"Invalid operation")
            return
        res = room.field.attack(self.resolver.get_id(), id, self.resolver.get_attack(), self.resolver.get_injured())
        if res == -1:
            conn.send(b'Not your round')
        elif res == -2:
            conn.send(b'Not in the cards')
        elif res == -3:
            conn.send(b'attacked card not in the cards')
        elif res == 0:
            users[id].send(self.generator.attack(self.resolver.get_attack(), self.resolver.get_injured()))
        elif res == 1:
            users[id].send(self.generator.attack(self.resolver.get_attack(), self.resolver.get_injured()))
            socks[conn].end()
            socks[users[id]].end()
            room.end_game()
            socks[conn].win()
            socks[users[id]].lose()
            conn.send(self.generator.game_over(0))
            users[id].send(self.generator.game_over(0))
        elif res == 2:
            users[id].send(self.generator.attack(self.resolver.get_attack(), self.resolver.get_injured()))
            socks[conn].end()
            socks[users[id]].end()
            room.end_game()
            socks[conn].win()
            socks[users[id]].lose()
            conn.send(self.generator.game_over(1))
            users[id].send(self.generator.game_over(1))

    def round_end(self, conn):
        room = rooms[self.resolver.get_room_num()]
        res = room.field.round_end(self.resolver.get_id(), self.resolver.get_time())
        print("res,", res)
        if res > 0:
            users[res].send(self.generator.round_over())
        else:
            conn.send(b'not your round')


class TCPServer:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("server is on")
        self.start_server()
        self.executor = Executor()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        """cause the conn is not blocking, so try to get the recv_message, if the data does not obey the form or the
        time exceed the limitation, the conn will be rejected"""
        try:
            data = conn.recv(1024)
        except:
            self.quit(conn)
            return -1

        data = data.decode()

        if data:
            if not data.endswith('\r\n\r\n'):
                conn.send(b'Wrong format')
                sel.unregister(conn)
                conn.close()
                return -2
            data = data.replace('\r\n\r\n', '')
            data = data.split('\r\n')

            if len(data) < 2:
                conn.send(b'Wrong format')
                sel.unregister(conn)
                conn.close()
                return -2

            ctime = float(data[0].split(' ')[1])

            if time.time() - ctime > 3.5:
                conn.send(b'Time exceed')
                return -3
            try:
                print(data)
                self.executor.execute(data, conn)
            except:
                try:
                    conn.send(b'Unresolvable message')
                    # self.close_sock(conn)
                except:
                    pass
                return -4
        else:
            try:
                self.quit(conn)
            except:
                pass
            return -1

    def quit(self, conn):
        try:
            player = socks[conn]
            fr_li = player.get_friend_list()
            for i in fr_li:
                if fr_li[i][1] == 1:
                    try:
                        socks[users[names[i]]].friend_out_room(socks[conn].get_name())
                        users[names[i]].send('{} outline'.format(player.get_name()).encode())
                    except:
                        pass
            if player.get_status() == 1:
                player.outline()
                conn_db.log_out(player.get_id())
                del users[player.get_id()]
                del socks[conn]
                del player
            if player.get_status() == 2 or player.get_status() == 3:
                player.outline()
                res = rooms[player.get_room()].delete_player(player.get_id())
                if res == 2:
                    del rooms[player.get_room()]
                conn_db.log_out(player.get_id())
                del users[player.get_id()]
                del socks[conn]
                del player
            elif player.get_status() == 4:
                pass

        except:
            pass
        sel.unregister(conn)
        conn.close()

    def start_server(self):
        self.sock.bind(('', 14290))
        self.sock.listen(100)
        self.sock.setblocking(False)
        res = conn_db.get_user_list()
        print(res)
        '''get names'''
        for r in res:
            names[r[1]] = r[0]
        res = conn_db.get_card()
        print(res)
        for r in res:
            cards[r[0]] = Games.Card(r[0], r[1], r[2], r[3])
        sel.register(self.sock, selectors.EVENT_READ, self.accept)


def send(id, msg):
    sock = users[id]
    sock.send(msg)


def run():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    server = TCPServer()
    run()

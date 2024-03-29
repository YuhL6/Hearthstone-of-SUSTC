import time


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
        """valid only when register, log, change password"""
        return int(self._id)

    def get_method(self):
        """valid any time"""
        return self._method

    def get_time(self):
        """valid any time"""
        return self._time

    def get_password(self):
        """valid when log, register and change password"""
        return self.data[1].split(' ')[1]

    def get_user_name(self):
        """only valid in register"""
        try:
            return self.data[2]
        except:
            return None

    def get_email(self):
        """only register"""
        try:
            email = self.data[3]
            if email != '':
                return email
            else:
                return None
        except:
            return None

    def get_new_password(self):
        """only change password"""
        return self.data[2]

    def get_list_name(self):
        return self.data[1].split(' ')[1]

    def get_card_name(self):
        return int(self.data[2])

    def get_room_num(self):
        return int(self.data[1].split(' ')[1])

    def get_receiver(self):
        """valid in friend system
        friend system includes: request, accept, refuse, send message, delete"""
        return self.data[1].split(' ')[1]

    def get_sender(self):
        """friend system"""
        return self.data[1].split(' ')[1]

    def get_delete_name(self):
        return self.data[1].split(' ')[1]

    def get_delete_num(self):
        return self.data[1].split(' ')[1]

    def get_message(self):
        """only in send message"""
        return self.data[2]

    def get_card(self):
        return int(self.data[2])

    def get_attack(self):
        return int(self.data[2].split(' ')[0])

    def get_injured(self):
        return int(self.data[2].split(' ')[1])

    def get_side(self):
        return int(self.data[2])


class Generator:
    def __init__(self):
        pass

    def wrong_access(self, reason):
        str = '000 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str.encode()

    def friend_online(self, name):
        str = '100 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def friend_outline(self, name):
        str = '101 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def friend_in_room(self, name):
        str = '102 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def friend_out_room(self, name):
        str = '103 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def friend_in_game(self, name):
        str = '104 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def friend_out_game(self, name):
        str = '105 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        str = str.encode()
        return str

    def new_room(self, room_id, room_owner):
        str = '106 {}\r\n'.format(time.time())
        str += '{} {}\r\n'.format(room_id, room_owner)
        str += '\r\n'
        return str.encode()

    def delete_room(self, room_id):
        str = '107 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def room_full(self, room_id):
        str = '108 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def room_empty(self, room_id):
        str = '109 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def room_start_game(self, room_id):
        str = '110 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def room_end_game(self, room_id):
        str = '111 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def owner_change(self, room_id, name):
        str = '112 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '{}\r\n'.format(name)
        str += '\r\n'
        return str.encode()

    def player_in(self, room_id, name):
        str = '113 {}\r\n'.format(time.time())
        str += '{} {}\r\n'.format(room_id, name)
        str += '\r\n'
        return str.encode()

    def player_out(self, room_id):
        str = '114 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def player_ready(self, room_id):
        str = '115 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()

    def player_not_ready(self, room_id):
        str = '116 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(room_id)
        str += '\r\n'
        return str.encode()


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

    def log_success(self, li: list, fr, un):
        st = '212 {}\r\n'.format(time.time())
        for e in li:
            st += '{} {} {}\r\n'.format(e[0], e[1], e[2])
        st += '{}\r\n'.format(len(fr))
        for l in fr:
            st += '{} {} {}'.format(l, fr[l][0], fr[l][1])
            st += '\r\n'
        st += '{}\r\n'.format(len(un))
        for l in un:
            st += str(l)
            st += '\r\n'
        st += '\r\n'
        print('st: ', st)
        return st.encode()

    def change_pass_fail(self, reason):
        str = '221 {}\r\n'.format(time.time())
        str += reason
        str += '\r\n\r\n'
        return str.encode()

    def change_pass_suc(self):
        str = '222 {}\r\n'.format(time.time())
        str += '\r\n'
        return str.encode()

    def request(self, name):
        str = '400 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        return str.encode()

    def request_fail(self, name, reason):
        str = '401 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def add_success(self, name, status):
        str = '402 {}\r\n'.format(time.time())
        str += '{} {}\r\n\r\n'.format(name, status)
        return str.encode()

    def accept_fail(self, name, reason):
        str = '411 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def refuse_fail(self, name, reason):
        str = '416 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def send_msg(self, name, msg):
        str = '420 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(msg)
        return str.encode()

    def send_msg_fail(self, name, reason):
        str = '421 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def delete_fail(self, name, reason):
        str = '431 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(name)
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def delete_success(self, name):
        str = '432 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        return str.encode()

    def deleted(self, name):
        str = '433 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(name)
        return str.encode()

    def list_room(self, rooms):
        str = '502 {}\r\n'.format(time.time())
        str += '{}\r\n'.format(len(rooms))
        for r in rooms:
            str += '{} {} {}\r\n'.format(r, rooms[r].get_status(), rooms[r].get_owner_name())
        str += '\r\n'
        return str.encode()

    def create_room_fail(self, reason):
        str = '511 {}\r\n'.format(time.time())
        str += '{}\r\n\r\n'.format(reason)
        return str.encode()

    def create_room_suc(self, room_id):
        str = '512 {}\r\n{}\r\n\r\n'.format(time.time(), room_id)
        return str.encode()

    def add_room_fail(self, reason):
        str = '521 {}\r\n'.format(time.time())
        str += '{} {}\r\n'.format(room_id, reason)
        str += '\r\n'
        return str.encode()

    def add_room_suc(self, room_id, owner_name):
        str = '522 {}\r\n'.format(time.time())
        str += '{} {}\r\n'.format(room_id, owner_name)
        str += '\r\n'
        return str.encode()

    def ready_fail(self, room_id, reason):
        str = "531 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, reason)
        return str.encode()

    def ready_suc(self, room_id):
        str = "532 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(room_id)
        return str.encode()

    def cancle_ready_fail(self, room_id, reason):
        str = "536 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, reason)
        return str.encode()

    def cancel_ready_suc(self, room_id):
        str = "537 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(room_id)
        return str.encode()

    def leave_room_fail(self, room_id, reason):
        str = "546 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, reason)
        return str.encode()

    def leave_room_suc(self, room_id):
        str = "547 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(room_id)
        return str.encode()

    def start_game_fail(self, room_id,reason):
        str = "551 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, reason)
        return str.encode()

    def start_game_suc(self, room_id, priority, li: list):
        str = "552 {}\r\n".format(time.time())
        str += "{} {}\r\n".format(room_id, priority)
        str += "Defaultuser0\r\n"
        str += "Defaultuser1\r\n"
        print(li)
        for i in li:
            str += "{}\r\n".format(i)
        str += "\r\n"
        print(str)
        return str.encode()

    def msg_in_room(self, room_id, msg):
        str = "570 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, msg)
        return str.encode()

    def put_card_fail(self, room_id, reason):
        str = "581 {}\r\n".format(time.time())
        str += "{}\r\n{}\r\n\r\n".format(room_id, reason)
        return str.encode()

    def put_card_suc(self, card_id):
        str = "582 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(card_id)
        return str.encode()

    def attack(self, a, b):
        str = "592 {}\r\n".format(time.time())
        str += "{} {}\r\n\r\n".format(a, b)
        return str.encode()

    def game_over(self, side):
        str = "610 {}\r\n".format(time.time())
        str += "{}\r\n\r\n".format(side)
        return str.encode()

    def round_over(self):
        str = "602 {}\r\n\r\n".format(time.time())
        return str.encode()

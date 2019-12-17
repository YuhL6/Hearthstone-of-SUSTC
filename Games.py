import random


class Player:
    def __init__(self, id, socket, time, li, res):
        """
        user log in, change the status stored in the database and get information from database
        inform all the friends, use the method broadcast of TCP server.
        status 1 means online, 2 means in room, 3 means ready, 4 means gaming

        """

        self._id = id
        self._status = 1
        self.socket = socket
        self._friends_list = res
        self._room = -1
        self.last_time = time
        self._name = li[0]
        self._total_game_num = li[1]
        self._win_rate = li[2]

    def get_room(self):
        return self._room

    def get_id(self):
        return self._id

    def get_status(self):
        return self._status

    def get_name(self):
        return self._name

    def get_friend_list(self):
        return self._friends_list

    def friend_online(self, name):
        self._friends_list[name][1] = 1

    def friend_outline(self, name):
        self._friends_list[name][1] = 0

    def friend_in_room(self, name):
        self._friends_list[name][1] = 2

    def friend_in_game(self, name):
        self._friends_list[name][1] = 3

    def friend_out_game(self, name):
        self._friends_list[name][1] = 2

    def friend_out_room(self, name):
        self._friends_list[name][1] = 1

    def add_friend(self, name):
        self._friends_list[name] = ['', 1]

    def delete_friend(self, name):
        del self._friends_list[name]

    def in_room(self, room_id):
        if self._status >= 2:
            return -1
        self._status = 2
        self._room = room_id
        return 0

    def out_room(self):
        if self._status != 2 and self._status != 3:
            return -1
        self._status = 1
        return 0

    def ready(self):
        if self._status != 2:
            return -1
        self._status = 3
        return 0

    def not_ready(self):
        if self._status != 3:
            return -1
        self._status = 2
        return 0

    def start(self):
        if self._status != 3:
            return -1
        self._status = 4
        return 0

    def undo_start(self):
        if self._status != 4:
            return -1
        self._status = 3
        return 0

    def end(self):
        if self._status != 4:
            return -1
        self._status = 2
        return 0

    def win(self):
        self._win_rate = (self._total_game_num * self._win_rate + 1) / (self._total_game_num + 1)
        self._total_game_num += 1

    def lose(self):
        self._win_rate = (self._total_game_num * self._win_rate - 1) / (self._total_game_num - 1)
        self._total_game_num -= 1

    def outline(self):
        self._status = 0


class Room:
    def __init__(self, id, owner_id, owner_name, password=None):
        """
        status: 0 means empty, 1 means full, 2 means ready, 3 means gaming
        if the owner set password, any one who wants to add into the room needs to enter the password

        """
        self._id = id
        self._owner = owner_id
        self._owner_name = owner_name
        self._attacker = -1
        self._attacker_name = ''
        self.field = None
        self._status = 0
        self._password = password

    def get_id(self):
        return self._id

    def get_owner(self):
        return self._owner

    def get_owner_name(self):
        return self._owner_name

    def get_attacker(self):
        return self._attacker

    def get_status(self):
        return self._status

    def add_player(self, player, player_name, password=None):
        if self._password != password:
            return -1
        if self._status != 0:
            return -2
        self._attacker = player
        self._attacker_name = player_name
        self._status = 1
        return 0

    def ready(self):
        if self._status != 1:
            return -1
        self._status = 2
        return 0

    def not_ready(self):
        if self._status != 2:
            return -1
        self._status = 1
        return 0

    def delete_player(self, player):
        """there are three different situations, the first is the attacker quit the room, the second is the owner quit
        the game and then the attacker inherit the room, the last one is that the room is deleted"""
        if self._status == 3:
            # Room is gaming
            return -1
        if player == self._attacker and self._status != 0:
            self._status = 0
            return 0
        if player == self._owner:
            if self._status == 1 or self._status == 2:
                self._owner = self._attacker
                self._owner_name = self._attacker_name
                self._status = 0
                # owner is changed
                return 1
            else:
                # room is deleted
                return 2

    def change_owner(self):
        """implemented only by owner"""
        if self._status < 1:
            # no attacker in this room
            return -1
        tmp = self._owner
        tmp_name = self._owner_name
        self._owner = self._attacker
        self._attacker = tmp
        self._attacker_name = tmp_name
        return 0

    def start_game(self, time):
        if self._status != 2:
            return -1
        self.field = Field(self.get_id(), time + 0.3)
        self._status = 3
        return 0

    def end_game(self):
        if self._status != 3:
            return -1
        del self.field
        self.field = None
        self._status = 2


class Card:
    def __init__(self, id, blood, attack, skill):
        self._id = id
        self._blood = blood
        self._attack = attack
        self._skill = skill

    def get_id(self):
        return self._id

    def get_blood(self):
        return self._blood

    def get_attack(self):
        return self._attack

    def get_skill(self):
        return self._skill

    def be_attacked(self, attack):
        self._blood = self._blood - attack
        if self._blood < 0:
            return -1
        else:
            return 0


class Field:
    class side:
        def __init__(self, id, index: list, cards: dict):
            self._id = id
            self.blood = 4.0
            self.cards_index = index
            self.cards = cards
            self.using = {}
            self.used = {}
            self.money = 1
            for i in range(3):
                cnt = index[0]
                print("cnt,", cnt)
                self.using[cnt] = cards[cnt]
                del index[0]
                del cards[cnt]

        def get_id(self):
            return self._id

        def get_card(self):
            index = self.cards_index[0]
            del self.cards_index[0]
            self.using[index] = self.cards[index]
            del self.cards[index]

        def put_card(self, c):
            try:
                card = self.using[c]
                del self.using[c]
                return card
            except:
                return None

    def __init__(self, id, time):
        self.room = id
        self.first = None
        self.last = None
        self.round = True  # True indicates first, false indicates last
        self.round_start_time = time
        self.first_field = {}
        self.last_field = {}
        ''''''

    def set_first(self, id, index, cards):
        self.first = self.side(id, index, cards)

    def set_last(self, id, index, cards):
        self.last = self.side(id, index, cards)

    def put_card(self, id, c):
        if self.round:
            if id != self.first.get_id():
                # not this round
                return -1
            card = self.first.put_card(c)
            if card is None:
                # not in the cards
                return -2
            try:
                self.first_field[c] = card
            except:
                # same card exists in the card
                return -3
        else:
            if id != self.last.get_id():
                return -1
            card = self.last.put_card(c)
            if card is None:
                # not in the cards
                return -2
            try:
                self.last_field[c] = card
            except:
                # same card exists in the card
                return -3
        return 0

    def attack(self, id0, id1, card_id0, card_id1):
        if self.round:
            if id0 != self.first.get_id() or id1 == self.first.get_id():
                # not this round
                return -1
            try:
                card = self.first_field[card_id0]
            except:
                # not in the cards
                return -2
            if card_id1 == -1:
                self.last.blood = self.last.blood - card.get_attack()
                if self.last.blood <= 0:
                    print("{} win".format(self.first.get_id()))
                    # first win
                    return 1
                return 0
            else:
                try:
                    card0 = self.last_field[card_id1]
                except:
                    return -3
                res = card0.be_attacked(card.get_attack())
                if res == -1:
                    print("{} die".format(card0.get_id()))
                    del self.last_field[card0]
                return 0
        else:
            if id0 != self.last.get_id() or id1 == self.last.get_id():
                # not this round
                return -1
            try:
                card = self.last_field[card_id0]
            except:
                # not in the cards
                return -2
            if card_id1 == -1:
                self.first.blood = self.first.blood - card.get_attack()
                if self.first.blood <= 0:
                    print("{} win".format(self.last.get_id()))
                    # last win
                    return 2
            else:
                try:
                    card0 = self.first_field[card_id1]
                except:
                    return -3
                res = card0.be_attacked(card.get_attack())
                if res == -1:
                    print("{} die".format(card0.get_id()))
                    del self.first_field[card0]
                return 0

    def round_end(self, id, time):
        if self.round:
            if self.first.get_id() == id:
                self.round = False
                self.round_start_time = time + 0.5
                self.last.get_card()
                return self.last.get_id()
            elif time - self.round_start_time >= 20 and self.last.get_id() == id:
                self.round = False
                self.last.get_card()
                self.round_start_time = time + 0.5
                return self.last.get_id()
        elif not self.round:
            if self.last.get_id() == id:
                self.round = True
                self.first.get_card()
                self.round_start_time = time + 0.5
                return self.first.get_id()
            elif time - self.round_start_time >= 20 and self.first.get_id() == id:
                self.round = True
                self.first.get_card()
                self.round_start_time = time + 0.5
                return self.first.get_id()
        return -1

    def end_time(self, player):
        if player == 0:
            self.owner_money += 1
        else:
            self.attacker_money += 1

    '''def game_over(self, room: Room, server):
        room.end_game(server)'''

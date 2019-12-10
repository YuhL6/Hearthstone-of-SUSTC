import random


class card:
    def __init__(self):
        card.num = 0
        card.attack = 0
        card.life = 0
        card.buff = 0b0000
        card.attr = 0b0000


available_room_num = []
max_room_num = 0


class Player:
    def __init__(self, id, socket, time, li, res):
        """
        user log in, change the status stored in the database and get information from database
        inform all the friends, use the method broadcast of TCP server

        """

        self._id = id
        # status 1 means online, 2 means in room, 3 means ready, 4 means gaming
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
        if self._status != 2:
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

    def start_game(self):
        if self._status != 2:
            # not ready
            return -1
        self.field = Field()
        self._status = 3
        return 0

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
        if self._status == 3:
            # Room is gaming
            return -1
        if player == self._attacker and self._status != 0:
            self._status = 0
            return 0
        elif player == self._attacker:
            # invalid operation
            return -2
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
        if self.status < 1:
            return -1
        tmp = self.owner
        self.owner = self.player
        self.player = tmp
        self.player.ready()

    '''def delete_room(self, server):
        self.owner.out_room(server)
        if self.status >= 1:
            self.player.out_room(server)
        id = self.id
        return id

    def delete_owner(self, server):
        if self.status < 1:
            self.delete_room(server)
            return 0
        self.owner.out_room(server)
        self.player.ready(server)
        self.owner = self.player
        self.player = None
        return 0

    def end_game(self, server):
        self.field = None
        self.owner.in_room(server)
        self.player.in_room(server)'''


class Field:
    def __init__(self, id, p1, p2):
        self.room = id
        self.owner_money = 1
        self.attacker_money = 1
        self.owner_hp = 4.0
        self.attacker_hp = 4.0
        self.owner_cards = []
        self.attacker_cards = []
        self.owner_field = []
        self.attacker_field = []
        self.owner_card_packet = p1
        self.attacker_card_packet = p2

    def pick_card(self, player):
        if player == 0:
            rest = len(self.owner_card_packet)
        else:
            rest = len(self.attacker_card_packet)
        rate = random.random() + 0.1
        card = rate * rest
        if player == 0:
            self.owner_cards.append(card)
            del self.owner_card_packet[card]
        else:
            self.attacker_cards.append(card)
            del self.attacker_card_packet[card]
        # send the card to the client
        return card

    def throw_card(self, player, card):
        if player == 0:
            # get the index of the card
            card = self.owner_cards.index(card)
            del self.owner_cards[card]
        else:
            card = self.attacker_cards.index(card)
            del self.attacker_cards[card]

    def end_time(self, player):
        if player == 0:
            self.owner_money += 1
        else:
            self.attacker_money += 1

    '''def game_over(self, room: Room, server):
        room.end_game(server)'''

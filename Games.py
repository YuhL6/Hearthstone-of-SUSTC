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
        return self._status

    '''def ready(self, server: Server.TCPServer):
        self._status = 3
        server.broadcast(self._friends_list, b'')

    def in_room(self, server: Server.TCPServer):
        self._status = 2
        server.broadcast(self._friends_list, b'')

    def out_room(self, server: Server.TCPServer):
        self._status = 1
        server.broadcast(self._friends_list, b'')

    def start_game(self, server: Server.TCPServer):
        self._status = 4
        server.broadcast(self._friends_list, b'')'''


class Room:
    def __init__(self, id, owner: Player, server, password=None):
        """
        status: 0 means empty, 1 means full, 2 means ready, 3 means gaming
        if the owner set password, any one who wants to add into the room needs to enter the password

        """
        self.id = id
        self.owner = owner
        self.owner.ready(server)
        self.player = None
        self.field = None
        self.status = 0
        self.password = password

    def start_game(self):
        if self.status != 2:
            # not ready
            return -1
        self.field = Field()
        self.status = 3
        return 0

    def add_player(self, player: Player, password=None):
        if self.password != password:
            return -1
        self.player = player
        self.status = 1
        return 0

    def ready(self):
        if self.status != 1:
            return -1
        self.status = 2
        self.player.ready()
        return 0

    def delete_player(self):
        if self.status == 3:
            # invalid operation
            return -2
        if self.status >= 1:
            # empty room
            return -1
        self.player = None
        self.status = 0

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

import MySQLdb


class Conn_DB:
    def __init__(self):
        self.database = MySQLdb.connect("localhost", "root", "123456", "ooad_proj", charset='utf8')
        self.cursor = self.database.cursor()
        print('connected')

    def get_user_list(self):
        mysql = 'select user_id, user_name from user_info where user_id > 10;'
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            res = list(results)
            return res
        except:
            return None

    def get_from_database(self, table, field, condition):
        """both select and condition are string, e.g. select: user_id; condition: user_id = 111111"""
        mysql = "select {} from {} where {};".format(field, table, condition)
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            res = []
            for i in results:
                res.append(list(i))
            return res
        except:
            return None

    def store_into_database(self, table, fields, data):
        mysql = "insert into {} {} values ({});".format(table, fields, data)
        print(mysql)
        try:
            self.cursor.execute(mysql)
            self.database.commit()
            return True
        except:
            self.database.rollback()
            return False

    def update(self, table, field, field_name, condition):
        mysql = 'update {} SET {}={} where {}'.format(table, field, field_name, condition)
        try:
            self.cursor.execute(mysql)
            self.database.commit()
            return True
        except:
            self.database.rollback()
            return False

    def check_duplicate(self, table, field, condition):
        mysql = 'select {} from {} where {};'.format(field, table, condition)
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            if len(results) == 0:
                return False
            else:
                return True
        except:
            print('what the hell')
            return None

    def get_friend_list(self, user_id):
        global res
        mysql = 'select b.user_name, a.name2, b.status from (select user_id2, name2 from relation where ' \
                'user_id1 = {}) a join user_info b on a.user_id2 = b.user_id;'.format(user_id)
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            res = {}
            for i in results:
                res[i[0]] = [i[1], i[2]]
        except:
            pass

        mysql = 'select b.user_name, a.name1, b.status from (select user_id1, name1 from relation where ' \
                'user_id2 = {}) a join user_info b on a.user_id1 = b.user_id;'.format(user_id)
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            for i in results:
                res[i[0]] = [i[1], i[2]]
        except:
            pass
        return res

    def get_user_info(self, user_id):
        res = self.get_from_database('user_info', 'user_name, total_game_num, win_rate', 'user_id={}'.format(user_id))
        return res

    def register(self, user_id, password, name, email):
        """first check whether user id or user name already exists, if not, execute the mysql, if something wrong
        happens, means the email duplicates"""
        if self.check_duplicate('user_info', 'user_id', 'user_id = {}'.format(user_id)):
            # id duplicate
            return -1
        if self.check_duplicate('user_info', 'user_name', 'user_name = \'{}\''.format(name)):
            # name duplicate
            return -2
        if email is not None and not email == '':
            mysql = '{}, \'{}\', \'{}\', \'{}\''.format(user_id, password, name, email)
            if self.store_into_database('user_info', '(user_id, password, user_name, user_email)', mysql):
                return 0
            else:
                # email duplicate
                return 1
        else:
            mysql = '{}, \'{}\', \'{}\''.format(user_id, password, name)
            if self.store_into_database('user_info', '(user_id, password, user_name)', mysql):
                return 0

    def log(self, user_id, password):
        res = self.get_from_database('user_info', 'password', 'user_id = {}'.format(user_id))
        if len(res) == 0:
            # no such user_id
            return -1
        reference = res[0][0]
        if reference == password:
            # change the status of the user
            self.update('user_info', 'status', 1, 'user_id={}'.format(user_id))
            return 0
        else:
            return -2

    def change_password(self, user_id, password):
        return self.update('user_info', 'password', password, 'user_id={}'.format(user_id))

    def log_out(self, user_id):
        self.update('user_info', 'status', 0, 'user_id={}'.format(user_id))

    def add_relation(self, user_id1, user_id2, name1='', name2=''):
        mysql = '{}, \'{}\', {}, \'{}\''.format(user_id1, name1, user_id2, name2)
        self.store_into_database('relation', '(user_id1, name1, user_id2, name2)', mysql)

    def delete_relation(self, id1, id2):
        mysql = 'delete from relation where (user_id1 = {} and user_id2 = {}) or (user_id1 = {} and user_id2 ' \
                '= {});'.format(id1, id2, id2, id1)
        try:
            self.cursor.execute(mysql)
            self.database.commit()
            return True
        except:
            self.database.rollback()
            return False

    def get_card(self):
        res = self.get_from_database('cards', '*', 'id > 0')
        return res

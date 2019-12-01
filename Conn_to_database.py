import MySQLdb


class Conn_DB:
    def __init__(self):
        self.database = MySQLdb.connect("localhost", "root", "123456", "ooad_proj", charset='utf8')
        self.cursor = self.database.cursor()
        print('connected')

    def get_from_database(self, table, field, condition):
        """both select and condition are string, e.g. select: user_id; condition: user_id = 111111"""
        mysql = "select {} from {} where {};".format(field, table, condition)
        res = []
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            for row in results:
                res.append(row)
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

    def register(self, user_id, password, name, email):
        """first check whether user id or user name already exists, if not, execute the mysql, if something wrong
        happens, means the email duplicates"""
        if self.check_duplicate('user_info', 'user_id', 'user_id = {}'.format(user_id)):
            # id duplicate
            return -1
        if self.check_duplicate('user_info', 'user_name', 'user_name = \'{}\''.format(name)):
            # name duplicate
            return -2
        mysql = '{}, \'{}\', \'{}\', \'{}\''.format(user_id, password, name, email)
        if self.store_into_database('user_info', '(user_id, password, user_name, user_email)', mysql):
            return 0
        else:
            # email duplicate
            return 1

    def log(self, user_id, password):
        """mysql = "select face_id from user_information where user_id = {};".format(self.user_id)
        try:
            self.cursor.execute(mysql)
            results = self.cursor.fetchall()
            for row in results:
                reference = row[0]
                break
            if reference == password:
                return "200 successfully done"
            else:
                return "404 not the same person"
        except:
            return "405 user_id not exists\""""
        res = self.get_from_database('user_info', 'password', 'user_id = {}'.format(user_id))
        print(res)
        if res is None:
            # no such user_id
            return 0
        reference = res[0][0]
        if reference == password:
            # change the status of the user
            # self.update('user_info', 'status', 1, 'user_id={}'.format(user_id))
            return 2
        else:
            return 1

    def get_friend_list(self, user_id):
        res = self.get_from_database('relation', 'user_id2', 'user_id1={}'.format(user_id))
        res = res.append(self.get_from_database('relation', 'user_id1', 'user_id2={}'.format(user_id)))
        return res

    def get_user_info(self, user_id):
        res = self.get_from_database('user_info', 'user_name, total_game_num, win_rate', 'user_id={}'.format(user_id))[0]
        return res

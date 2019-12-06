import socket
import time
import random
def connection():
    ServerIP = '122.51.26.166'
    ServerPort = 14290
    a = 0
    time1 = time.time()
    sockets = []
    cnt = 0
    for i in range(100):
        ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ServerSocket.connect(('127.0.0.1', 14290))
        ServerSocket.send(b'123\r\n\r\n')
        time.sleep(0.01)
        Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        Socket.connect(('127.0.0.1', 14290))
        Socket.send(b'123\r\n\r\n')
        ServerSocket.send(b'111111')
        '''ServerSocket.send(b'12345')
        time.sleep(0.1)
        ServerSocket.send(b'123456')'''
        sockets.append(ServerSocket)
        sockets.append(Socket)
        print(cnt)
        cnt += 1
    time.sleep(5)
    while True:
        index = random.randint(0, 99)
        sock = sockets[index]
        print(sock)
        sock.send(b'hahaha, r u ok?')
        time.sleep(10)
        sock.send(b'hahaha?')
        cnt += 1
        print(sock.getsockname(), '        ', cnt)
        time.sleep(0.01)

if __name__ == "__main__":
    connection()



'''time_stamp = float(data[0].split(' ')[-1])
current_time = time.time()
if current_time - time_stamp >= 300:
    return "400 time exceeds"
line = data[1].split(' ')
mysql = "select face_id from user_information where user_id = {};".format(self.user_id)
reference = str
try:
    cursor.execute(mysql)
    results = cursor.fetchall()
    for row in results:
        reference = row[0]
        break
    print("r", reference)
    reference = string_to_float_array(reference)
    print("r", reference)
    if len(self.face_id) == 0:
        return "404 current_time no face recognized"
    print("f", self.face_id)
    fresh = string_to_float_array(self.face_id)
    print("f", fresh)
    print(len(reference) == len(fresh))
    if calculate_distance(reference, fresh) < 0.6:
        return "200 current_time"
    else:
        return "400 current_time (wrong password)"
except:
    return "400 current_time (user_id not exists)'''
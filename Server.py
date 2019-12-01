import asyncio
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import random
import time
import threading
from multiprocessing import Pool, Process

ServerPort = 14290
users = {}
selector = DefaultSelector()
'''data = conn.recv(1024)
        data = data.split('/r/n')
        if data[0].split(' ') == '200':
            # check whether the information exists or not
            # add information to the database
            # return the information
            conn.close()
            continue
        if data[0].split(' ') == '210':
            # resolve the data, use the try exception
            user_id = 0
            try:
                temp = users[user_id]
            except:
                # send the invalid information
                conn.send()
            users[user_id] = User()
            # check the user information
    print(1)'''

'''async def worker(queue):
    while True:
        # Get a "work item" out of the queue.
        index = await queue.get()
        fsocket = sockets[index]
        print(index)
        data = await asyncio.wait_for(fsocket.recv(1024), timeout=0.1)
        print(data)
        # Notify the queue that the "work item" has been processed.
        queue.put_nowait(index)
        queue.task_done()'''

'''
async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    total_sleep_time = 0
    for i in range(len(sockets)):
        queue.put_nowait(i)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(3):
        task = asyncio.create_task(worker(queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    await queue.join()

    # Cancel our worker tasks.
    for task in tasks:
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)'''

'''async def server_listen():
    while True:
        ti = time.time()
        for i in users:
            if time.time() - users[i].last_time > 2:
                del users[i]
                # the i is disconnected and broadcast the news
            data = await asyncio.wait_for(users[i].socket.recv(1024), 0.01)
            # resolve and then execute the data
        if time.time() - ti < 1:
            time.sleep(1 + ti - time.time())'''


class Resolver:
    def __init__(self, data: list):
        self.method = int(data[0].split(' ')[0])
        self.time = int(data[0].split(' ')[0])
        self.id = int(data[1].split(' ')[0])


class Generator:
    def __init__(self):
        pass


class TCPServer:
    def __init__(self):
        self.sockets = []
        self.cnt = 0

    async def worker(self):
        while True:
            for sock in self.sockets:
                try:
                    data = sock.recv(1024)
                except:
                    continue
                if data:
                    print(data, '    ', sock, '        ', self.cnt)
                    self.cnt += 1
            await asyncio.sleep(0.0000000000000001)
            '''# Get a "work item" out of the queue.
            index = await self.queue.get()
            fsocket = self.sockets[index]
            # data = await asyncio.wait_for(fsocket.recv(1024), timeout=0.1)
            try:
                data = timer(0.01, fsocket.recv, 1024)
            except:
                self.queue.put_nowait(index)
                self.queue.task_done()
                continue
            if data is not None:
                print(data)
            # Notify the queue that the "work item" has been processed.
            self.queue.put_nowait(index)
            self.queue.task_done()'''
    def pr(self, socket):
        try:
            data = socket.recv(1024)
            print(data)
        except:
            pass

    async def listener(self, reader, writer):
        data = []
        while True:
            tmp = await reader.readline()
            tmp = tmp.decode()
            if tmp == '\r\n':
                break
            data.append(tmp)
        socket = writer.get_extra_info('socket')
        print(data, '     ', socket, '        ', self.cnt)
        self.sockets.append(socket)
        self.cnt += 1
        # await self.worker()
        selector.register(socket, EVENT_READ, self.pr(socket))


    def start_server(self):
        loop = asyncio.get_event_loop()
        coro = asyncio.start_server(self.listener, '', 14290)
        server = loop.run_until_complete(coro)
        # Serve requests until Ctrl+C is pressed
        print('Serving on {}'.format(server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        # Close the server
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

    def send(self, id, msg):
        User = users[id]
        sock = User.socket
        sock.send(msg)

    def broadcast(self, li: list, msg):
        for i in li:
            self.send(i, msg)


if __name__ == '__main__':
    server = TCPServer()
    server.start_server()

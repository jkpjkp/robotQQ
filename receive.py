import socket
import json

ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)

HttpResponseHeader = '''HTTP/1.1 200 OK\r\n
Content-Type: text/html\r\n\r\n
'''


def recv_end(the_socket):
    total_data = bytes()
    while True:
        data = the_socket.recv(1024)
        total_data += data
        if total_data[-2] == 125 and total_data[-1] == 10:
            break
    return total_data.decode(encoding='utf-8')


def request_to_json(msg):
    for i in range(len(msg)):
        if msg[i] == '{' and msg[-1] == '\n':
            return json.loads(msg[i:])
    return None


# 需要循环执行，返回值为json格式
def rev_msg():  # json or None
    Client, Address = ListenSocket.accept()
    Request = recv_end(Client)
    rev_json = request_to_json(Request)
    Client.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    Client.close()
    return rev_json

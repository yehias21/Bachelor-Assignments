import time, socket, threading, webbrowser
from httphandler import *
def client_handler(client):
    while True:
        data=recv(client)
        parsed = parser(data,True)
        response=requesthandle(parsed)
        client.send(response)
        if parsed['protocol'] == 'HTTP/1.1':
            client.close()
            print(f"({time.ctime()}) - {parsed['method']} - {parsed['uri']}")
            break
            #todo: timeout handling heuristics
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port =8080
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            client, addr = s.accept()
            threading.Thread(target=client_handler, args=(client,)).start()
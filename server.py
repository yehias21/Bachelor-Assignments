import time, socket, threading, webbrowser
from httphandler import *
from concurrent.futures import ThreadPoolExecutor
print_lock = threading.Lock()
qLock=threading.Lock()
def client_handler(client,exe):
    time_started = time.time()
    parsed={}
    while True:
        data=recv(client)
        if data!=b'':
            arr = parser(data,True)
            for parsed in arr:
                response=requesthandle(parsed)
                client.send(response)
                with print_lock:
                    print(f"{parsed['method']} /{parsed['uri']} {parsed['protocol']} - tid: {threading.current_thread().ident}")
        if parsed['protocol'] == 'HTTP/1.0':
            client.close()
            with print_lock:
                print(f"time: {round(time.time()-time_started,2)}")
            break
        elif parsed['protocol'] == 'HTTP/1.1':
            with qLock:
                if time.time() > time_started + 5/max(1,exe._work_queue.qsize()-8) :
                    client.close()
                    with print_lock:
                        print(f"Thread({threading.current_thread().ident}) finished in: {round(time.time() - time_started, 2)}")
                    break
                elif data!=b"":
                    time_started = time.time()

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        host = '127.0.0.1'
        port =8080
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        count=1
        with ThreadPoolExecutor(max_workers=8) as executor:
            while True:
                client, addr = s.accept()
                executor.submit(client_handler,client,executor)
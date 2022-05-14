from httphandler import *
from socket import *
def client():
    host = '127.0.0.1'
    port = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    with open('commands.txt') as file:
        for line in file.readlines():
            line=line.split()
            if line[0]=='HTTP/1.0':
                for command in line[1:]:
                    s.connect((host, port))
                    request=generaterequest(command)
                    s.send(request)
                    response=recv(s)
                    parsed=parser(response,False)
                    if command.lower().find('get',0,4):
                        with open(parsed['uri'], 'wb') as f:
                            f.write(parsed['data'])
                    print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                    s.close()
            elif line[0]=='HTTP/1.1':
                for command in line[1:]:
                    request = generaterequest(command)
                    s.send(request)
                for command in line[1:]:
                    response = recv(s)
                    parsed=parser(response,False)
                s.close()

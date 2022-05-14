from httphandler import *
import socket
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    with open('commands.txt') as file:
        for line in file.readlines():
            line=line.split(';')
            if line[0]=='HTTP/1.0':
                for command in line[1:]:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((host, port))
                    request=generaterequest(command,host,protocol='HTTP/1.0')
                    if request=='':
                        print('')
                        continue
                    s.send(request)
                    response=recv(s)
                    parsed=parser(response,False)
                    parsed=parsed[0]
                    print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                    s.close()
            elif line[0] == 'HTTP/1.1':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                for command in line[1:]:
                    request = generaterequest(command,host,protocol='HTTP/1.1')
                    if request=='':
                        print('')
                        continue
                    s.send(request)
                    response = recv(s)
                    parsed = parser(response, False)
                    parsed=parsed[0]
                    print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                s.close()
            elif line[0]=='HTTP/1.1p':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                for command in line[1:]:
                    request = generaterequest(command,host,protocol='HTTP/1.1')
                    s.send(request)
                for command in line[1:]:
                    response = recv(s)
                    ar=parser(response,False)
                    for parsed in ar:
                        print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                s.close()

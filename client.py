from httphandler import *
import socket,pickle,sys
if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8080
    configDic = {}
    try:
        with open('cache/clientdict.config', 'rb') as config_dictionary_file:
            configDic = pickle.load(config_dictionary_file)
    except:
        pass
    f=''
    try:
        if len(sys.argv)<2:
            raise Exception("NO arg passed")
        f=sys.argv[1]
        with open(f) as file:
            pass
    except :
        print('problem opening the file, default destination is assigned')
        f= 'commands.txt'

    with open(f) as file:
        for line in file.readlines():
            line=line.split(';')
            if line[0]=='HTTP/1.0':
                for command in line[1:]:
                    method, file = command.split()
                    if method.lower() == 'get' and file in configDic:
                        print(f'file({file}) already cached!')
                        continue
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
                    if method.lower() == 'get':
                        clientCache(configDic,parsed,file)
                    print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                    s.close()
            elif line[0] == 'HTTP/1.1':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                for command in line[1:]:
                    method, file = command.split()
                    if method.lower() == 'get' and file in configDic:
                        print(f'file({file}) already cached!')
                        continue
                    request = generaterequest(command,host,protocol='HTTP/1.1')
                    if request=='':
                        print('')
                        continue
                    s.send(request)
                    response = recv(s)
                    parsed = parser(response, False)
                    parsed=parsed[0]
                    if method.lower() == 'get':
                        clientCache(configDic,parsed,file)
                    print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                s.close()
            elif line[0]=='HTTP/1.1p':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                for command in line[1:]:
                    method, file = command.split()
                    if method.lower() == 'get' and file in configDic:
                        print(f'file({file}) already cached!')
                        line.remove(command)
                        continue
                    request = generaterequest(command,host,protocol='HTTP/1.1')
                    s.send(request)
                for command in line[1:]:
                    response = recv(s)
                    ar=parser(response,False)
                    for parsed in ar:
                        clientCache(configDic,parsed,file)
                        print(parsed['protocol']+' '+parsed['status']+' '+parsed['message'])
                s.close()
    with open('cache/clientdict.config', 'wb') as config_dictionary_file:
        pickle.dump(configDic, config_dictionary_file)

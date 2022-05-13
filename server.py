import os, sys, re, time, datetime, json, socket, threading, webbrowser
def load_config(filename):
    '''Open config file in JSON format'''
    with open(filename) as f:
        config = json.load(f)
        return config
config       = load_config('config.json')
http_status  = config['http_status']
content_type = config['content_type']
sep          = config['sep']

def open_static(filename, mode='r'):
    '''Opens static file and returns it\'s binary representation'''
    try:
        with open(filename, mode) as f:
            data = f.read()
            ts = os.stat(filename).st_mtime
            last_modified = datetime.datetime \
                .utcfromtimestamp(ts) \
                .strftime('%a, %d %b %Y %H:%M:%S GMT')
            return data, last_modified
    except:
        return b'', 0
# def writeit(filename,)
def build_header(status, file_type, last_modified,length):
    last_modified = f'Last-Modified: {last_modified}'
    content_length=f'Content-Length: {length}'+sep
    if length==0:
        content_length=''
    return http_status[status] + sep \
        + content_type[file_type]+ sep \
        + content_length\
        + last_modified + sep + sep
def requesthandle(request):
    if request['method'] == 'GET':
        body, last_modified = open_static(request['uri'], 'rb')
        if body:
            header = build_header('200', request['uri'], last_modified,len(body))
            return header+body
        else:
            header = build_header('404', request['uri'], last_modified,0)
            return header
    # elif request['method']=='POST':
#         try:
#             with open( 'w') as f:
#                 f.write('readme')
#                 build_header('200', request['uri'])

def parse_request(request):
    parsed = {}
    buff=request.split('\r\n')
    line=buff[0].split()
    parsed['method']=line[0]
    parsed['uri']=line[1]
    parsed['protocol'] = line[-1]
    for head in buff[1:]:
        head=head.split(":")
        if head==['']: break
        parsed[head[0]] = head[1].replace(" ", "")
    buff=request.split('\r\n\r\n')
    if 'Content-Length' in parsed.keys():
        parsed['data']=buff[1][:int(parsed['Content-Length'])]
    return parsed
def iscomplete(data):
    data=data.decode('utf-8')
    buff=data.split('\r\n\r\n')
    size=-1
    if buff[0]!=data:
        x=re.search('Content-Length: (.*)\r\n', data)
        if x is not None:
            size=int(x.group(1))
            if size==0:
                return -1
            elif size>len(buff[1]):
                return len(buff[1])-size
        else:
            return 0
    return -1
def recv(clsck,timeout=2):
    # make socket non blocking
    clsck.setblocking(0)
    data = ''
    begin = time.time()
    buffSize=1024
    while True:
        if data and time.time() - begin > timeout:
            break
        elif time.time() - begin > timeout * 2:
            break
        try:
            buff = clsck.recv(buffSize)
            if buff:
                data+=(buff)
                if iscomplete(data)==0:
                    return data
                elif iscomplete(data)>0:
                    buffSize=iscomplete(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return data
def client_handler(client):
    while True:
        data=recv(client)
        request = data
        print(request)
        parsed = parse_request(request)
        response=requesthandle(request)
        client.send(response)
        if parsed['protocol'] == 'HTTP/1.0':
            client.close()
            print(f"({time.ctime()}) - {parsed['method']} - {parsed['uri']}")
            break
            #todo: timeout handling heuristics
if __name__ == '__main__':

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Host 127.0. 0.1 means for localhost
        host = '127.0.0.1'
        port =8081
        # Bind socket to the desired address
        s.bind((host, port))
        # Listen for incoming messages
        s.listen()
        # Shows introduction to the terminal
        webbrowser.open(f'http://localhost:{port}')
        # Server is going to run until something breaks
        while True:
            client, addr = s.accept()
            # todo:thread pool
            threading.Thread(target=client_handler, args=(client,)).start()


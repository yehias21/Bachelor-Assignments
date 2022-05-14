import os, time, datetime, json
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
def build_header(status, file_type, last_modified='',length=0):
    modified = f'Last-Modified: {last_modified}'+ sep
    content_length=f'Content-Length: {length}'+sep
    if length==0:
        content_length=''
    if last_modified=='':
        modified=''
    return http_status[status] + sep \
        + content_length \
        + modified + sep
def requesthandle(request):
    if request['method'] == 'GET':
        body, last_modified = open_static(request['uri'], 'rb')
        if body:
            header = build_header('200', request['uri'], last_modified,len(body))
            header = header.replace('HTTP/1.x', request['protocol'])
            header=header.encode('utf-8')
            return header+body
        else:
            header = build_header('404', request['uri'], last_modified,0)
            header = header.replace('HTTP/1.x', request['protocol'])
            header=header.encode('utf-8')
            return header
    elif request['method']=='POST':
        if request['data']!=b'':
            with open('dataServer'+'/'+request['uri'],'wb') as f:
                f.write(request['data'])
                header = build_header('200', request['uri'])
                header = header.replace('HTTP/1.x', request['protocol'])
                return header.encode('utf-8')
        else:
            header = build_header('404', request['uri'])
            header = header.replace('HTTP/1.x', request['protocol'])
            return header.encode('utf-8')
def parser(request,isrequest):
    parsed = {}
    if request.count(b'\r\n\r\n')==1:
        msg=request.split(b'\r\n\r\n')
        buff=msg[0].decode('utf-8').split('\r\n')
        line=buff[0].split()
        if isrequest:
            parsed['method']=line[0]
            parsed['uri']=line[1][1:]
            parsed['protocol'] = line[-1]
        else:
            parsed['protocol'] = line[0]
            parsed['status'] = line[1]
            parsed['message'] = " ".join(line[2:])
        for head in buff[1:]:
            head=head.split(":")
            parsed[head[0]] = head[1].replace(" ", "")
        parsed['data']=msg[1]
        return [parsed]
    else:
        splitted = request.split(b'\r\n\r\n')
        ar=[]
        parsed={}
        for msg in splitted[:-1]:
            buff = msg.decode('utf-8').split('\r\n')
            line = buff[0].split()
            if isrequest:
                parsed['method'] = line[0]
                parsed['uri'] = line[1][1:]
                parsed['protocol'] = line[-1]
            else:
                parsed['protocol'] = line[0]
                parsed['status'] = line[1]
                parsed['message'] = " ".join(line[2:])
            for head in buff[1:]:
                head = head.split(":")
                parsed[head[0]] = head[1].replace(" ", "")
            ar.append(parsed)
    return ar

def recv(the_socket, timeout=0.5):
    the_socket.setblocking(0)
    total_data = []
    begin = time.time()
    while True:
        if total_data and time.time() - begin > timeout:
            break
        elif time.time() - begin > timeout * 2:
            break
        try:
            data = the_socket.recv(1024)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            pass
    return b''.join(total_data)
def generaterequest(command,host,filepath='dataClient',protocol='HTTP/1.1'):
    method,file=command.split()
    if method.lower()=='get':
        request=f"GET /{file} {protocol}\r\nHost: {host}\r\n\r\n"
        return request.encode('utf-8')
    elif method.lower()=='post':
        request=f"POST /{file} {protocol}\r\nHost: {host}\r\n\r\n"
        data,_=open_static(filepath+'/'+file)
        if data=='':
            print(f'File: {file} not found!')
            return ''
        return request.encode('utf-8')+data

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
lol=add(2,5)
def add(x,y):
    return x+y
# if __name__ == '__main__':
    request_string = 'GET / HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8\r\n\r\n'
    parseit(request_string)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
# See PyCharm help at https://www.jetbrains.com/help/pycharm
# def iscomplete(data):
#     buff=data.split(b'\r\n\r\n')
#     size=-1
#     x=re.search(b'Content-Length: (.*)\r\n', data)
#     if x is not None:
#         size=int(x.group(1))
#         if size==0:
#             return -1
#         elif size>len(buff[1]):
#             return size-len(buff[1])
#         else:
#             return 0
#     else:
#         return 0
# def recv(clsck):
#     # make socket non blocking
#     buffSize=1024
#     data = b''
#     data+=(clsck.recv(buffSize))
#     if iscomplete(data) == 0:
#         return data
#     else:
#         buffSize=iscomplete(data)
#         data += clsck.recv(buffSize)
#         return data

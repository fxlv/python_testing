#!/usr/bin/env python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 22330))
server.listen(2000)

while True:
    connection, address = server.accept()
    print "Accepted connection from {}:{}".format(address[0],address[1])
    buff = connection.recv(50)
    if len(buff)>0:
        print ">>"
        print len(buff)
        print buff



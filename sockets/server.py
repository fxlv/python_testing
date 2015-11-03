#!/usr/bin/env python
import socket
import profig

cfg = profig.Config("server.conf")
cfg.init("listen.host", "localhost")
cfg.init("listen.port", 22330)
cfg.sync()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((cfg['listen.host'], cfg['listen.port']))
server.listen(2000)

print "Server running on {}:{}".format(cfg['listen.host'], cfg['listen.port'])

while True:
    connection, address = server.accept()
    print "Accepted connection from {}:{}".format(address[0],address[1])
    buff = connection.recv(50)
    if len(buff)>0:
        print ">>"
        print len(buff)
        print buff



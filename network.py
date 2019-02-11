# -*- coding: utf-8 -*-

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import ftplib
import socket
import threading


class Server:
    def __init__(self, port, address=""):
        self.socket = socket.socket()
        self.port = port
        self.address = address
        self.connected = False
        self.clients = {}
        self.thread = None
        self.active = False
        self.max_client = float("inf")

    def connect(self):
        try:
            self.socket.bind((self.address, self.port))
            self.connected = True
            return True
        except Exception:
            print("[lemapi] [WARNING] [Server.__init__] Unable to bind port " \
                + "'%s'" % self.port)
            return False

    def listen(self, max_con_tmp):
        while self.active:
            if len(self.clients) < self.max_client:
                self.socket.listen(max_connection)
                con, add = self.socket.accept()
                self.clients[add] = con

            print("[lemapi] [INFO] [Server.listen] Client '%s' connected" % add)

    def start(self, max_con_tmp=0):
        if self.connected:
            self.active = True
            self.thread = threading.Thread(target=self.listen, args=(max_con_tmp,))
            self.thread.start()
        else:
            print("[lemapi] [WARNING] [Server.start] Server not initialized yet!")

    def stop(self):
        if self.thread:
            self.active = False
            self.thread.join()

    def send_data(self, data, client=None):
        if self.connected:
            if clients:
                if client in self.clients:
                    self.clients[client].send(data.encode())
            else:
                for connection in tuple(self.clients.values()):
                    connection.send(data.encode())
        else:
            print("[lemapi] [WARNING] [Server.send_data] Server not initialized" \
                + " yet!")

    def receive_data(self, data, client, buffer=1024):
        if self.connected:
            if client in self.clients:
                return self.clients[client].recv(buffer)
        else:
            print("[lemapi] [WARNING] [Server.receive_data] Server not initialized" \
                + " yet!")

    def disconnect(self, client):
        if client in self.clients:
            self.clients[client].close()
            self.clients.pop(client)
        else:
            print("[lemapi] [WARNING] [Server.disconnect_client] No client " \
                + "'%s' connected!" % client)


class Client:
    def __init__(self, address, port):
        self.socket = socket.socket()
        self.address = address
        self.port = port
        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.address, self.port))
            self.connected = True
            return True
        except Exception:
            print("[lemapi] [WARNING] [Client.__init__] Unable to connect to " \
                + "server '%s' with port '%s'" % (self.address, self.port))
            return False

    def send_data(self, data):
        if self.connected:
            self.socket.send(data.encode())
        else:
            print("[lemapi] [WARNING] [Client.send_data] Client not initialized" \
                + " yet!")

    def receive_data(self, data, buffer=1024):
        if self.connected:
            return self.socket.recv(buffer)
        else:
            print("[lemapi] [WARNING] [Client.receive_data] Client not " \
                + "initialized yet!")

    def disconnect(self):
        if self.connected:
            self.socket.close()
            self.connected = False

# -*- coding: utf-8 -*-

from lemapi.util import rpi_only

__author__ = "Julien Dubois"
__version__ = "0.1.0"

import ftplib
import os
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
        self.socket.listen(max_con_tmp)

        while self.active:
            if len(self.clients) < self.max_client:
                con, add = self.socket.accept()
                self.clients[add] = con

                if self.active:
                    print("[lemapi] [INFO] [Server.listen] Client '%s' connected" \
                        % add[0])

    def start(self, max_con_tmp=0):
        if self.connected:
            self.active = True
            self.thread = threading.Thread(target=self.listen, args=(max_con_tmp,))
            self.thread.start()
        else:
            print("[lemapi] [WARNING] [Server.start] Server not initialized yet!")

    def stop(self):
        if self.thread:
            for client in tuple(self.clients):
                self.disconnect(client)

            self.active = False
            socket.socket().connect((self.address, self.port))
            self.thread.join()

    def send(self, data, client=None):
        if self.connected:
            if client:
                if client in self.clients:
                    self.clients[client].send(data)
            else:
                for connection in tuple(self.clients.values()):
                    connection.send(data)
        else:
            print("[lemapi] [WARNING] [Server.send_data] Server not initialized" \
                + " yet!")

    def receive(self, client, buffer=1024):
        if self.connected:
            if client in self.clients:
                return self.clients[client].recv(buffer)
        else:
            print("[lemapi] [WARNING] [Server.receive_data] Server not initialized" \
                + " yet!")

    def send_msg(self, msg, client=None):
        self.send(msg.encode(), client)

    def receive_msg(self, client, buffer=1024):
        s = self.receive(client, buffer)
        if s:
            return s.decode()
        return ""

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

    def connect(self, timeout=None):
        if timeout:
            self.socket.settimeout(timeout)
        try:
            self.socket.connect((self.address, self.port))
            self.connected = True
            return True
        except Exception:
            print("[lemapi] [WARNING] [Client.__init__] Unable to connect to " \
                + "server '%s' with port '%s'" % (self.address, self.port))
            if self.connected:
                self.socket.close()
            self.connected = False
            return False

    def send(self, data):
        if self.connected:
            self.socket.send(data)
        else:
            print("[lemapi] [WARNING] [Client.send] Client not initialized" \
                + " yet!")

    def receive(self, buffer=1024):
        if self.connected:
            return self.socket.recv(buffer)
        else:
            print("[lemapi] [WARNING] [Client.receive] Client not " \
                + "initialized yet!")

    def send_msg(self, data):
        self.send(data.encode())

    def receive_msg(self, buffer=1024):
        s = self.receive(buffer)
        if s:
            return s.decode()
        return ""

    def disconnect(self):
        if self.connected:
            self.socket.close()
            self.connected = False

class Wifi:
    @staticmethod
    @rpi_only
    def disable():
        os.system("dhclient -r wlan0")
        os.system("ifdown wlan0")
        os.system("dhclient -v wlan0")

    @staticmethod
    @rpi_only
    def enable():
        os.system("dhclient -r wlan0")
        os.system("ifup wlan0")
        os.system("dhclient -v wlan0")

    @staticmethod
    @rpi_only
    def get_current_ssid():
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "r") as file:
            content = file.read()
            content = content.split("ssid=")[1]
            content = content.split("\"")[1]
        return content

    @staticmethod
    @rpi_only
    def add_network(ssid, psk, priority=None):
        with open("/etc/wpa_supplicant/{ssid}".format(ssid=ssid), "w") as file:
            file.write("country=FR\n")
            file.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
            file.write("update_config=1\n")
            file.write("network={\n")
            file.write('  ssid="{ssid}"\n'.format(ssid=ssid))
            file.write('  psk="{psk}"\n'.format(psk=psk))
            if priority:
                file.write('  priority={priority}\n'.format(priority))
            file.write("}\n")

    @staticmethod
    @rpi_only
    def connect(ssid):
        path = "/etc/wpa_supplicant/{ssid}".format(ssid=ssid)

        if os.path.exists(path):
            with open(path, "r") as file:
                content = file.read()
            with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as file:
                file.write(content)

            os.system("dhclient -r wlan0")
            os.system("ifdown wlan0")
            os.system("ifup wlan0")
            os.system("dhclient -v wlan0")
        else:
            print("[lemapi] [WARNING] [Wifi.connect] Unknown ssid '{ssid}'".format(ssid=ssid))
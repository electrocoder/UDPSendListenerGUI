#!/usr/bin/env python3

"""
UDPSendListenerGUI.py

Python UDP GUI

Author: electrocoder
Date: 14.08.2019
Website: www.iothook.com
"""

from tkinter import *
from tkinter.ttk import Frame, Button, Label
import socket
import threading
import configparser


class Window(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.master.title("UDPSendListenerGUI")
        self.pack(fill=BOTH, expand=True)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.columnconfigure(1, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(5, pad=7)

        self.is_connect = False

        self.client_ip_label = Label(self, text="Client IP")
        self.client_ip_label.grid(row=0, column=0, padx=10, sticky=E + W + S + N)

        self.client_ip_entry = Entry(self)
        self.client_ip_entry.grid(row=0, column=1, padx=10, sticky=E + W + S + N)

        self.client_port_label = Label(self, text="Client Port")
        self.client_port_label.grid(row=0, column=2, padx=10, sticky=E + W + S + N)

        self.client_port_entry = Entry(self, width=5)
        self.client_port_entry.grid(row=0, column=3, padx=10, sticky=E + W + S + N)

        self.local_port_label = Label(self, text="Local Port")
        self.local_port_label.grid(row=0, column=4, padx=10, sticky=E + W + S + N)

        self.local_port_entry = Entry(self, width=5)
        self.local_port_entry.grid(row=0, column=5, padx=10, sticky=E + W + S + N)

        self.connect_button = Button(self, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=6, padx=10, sticky=E + W + S + N)

        self.received_label = Label(self, text="Received data")
        self.received_label.grid(row=1, column=0, padx=10, sticky=E + W + S + N)

        self.received_text = Text(self, height=10)
        self.received_text.grid(row=2, column=0, columnspan=7, padx=10, sticky=E + W + S + N)

        self.sent_label = Label(self, text="Sent data")
        self.sent_label.grid(row=3, column=0, padx=10, sticky=E + W + S + N)

        self.sent_text = Text(self, height=10)
        self.sent_text.grid(row=4, column=0, columnspan=7, padx=10, sticky=E + W + S + N)

        self.send1_entry = Entry(self)
        self.send1_entry.grid(row=5, column=0, padx=10, columnspan=5, sticky=E + W + S + N)

        self.send1_button = Button(self, text="Send 1", command=self.send_1, state=DISABLED)
        self.send1_button.grid(row=5, column=5, padx=10, columnspan=2, sticky=E + W + S + N)

        self.send2_entry = Entry(self)
        self.send2_entry.grid(row=6, column=0, padx=10, columnspan=5, sticky=E + W + S + N)

        self.send2_button = Button(self, text="Send 2", command=self.send_2, state=DISABLED)
        self.send2_button.grid(row=6, column=5, padx=10, columnspan=2, sticky=E + W + S + N)

        self.send3_entry = Entry(self)
        self.send3_entry.grid(row=7, column=0, padx=10, columnspan=5, sticky=E + W + S + N)

        self.send3_button = Button(self, text="Send 3", command=self.send_3, state=DISABLED)
        self.send3_button.grid(row=7, column=5, padx=10, columnspan=2, sticky=E + W + S + N)

        self.cfg_file = "udp.ini"
        try:
            config = configparser.ConfigParser()
            config.read_file(open(self.cfg_file))

            self.client_ip = config['SETTINGS']['client_ip']
            self.client_port = config['SETTINGS']['client_port']
            self.local_port = config['SETTINGS']['local_port']

            self.client_ip_entry.insert(END, self.client_ip)
            self.client_port_entry.insert(END, self.client_port)
            self.local_port_entry.insert(END, self.local_port)

            self.send1_entry.insert(END, config['SETTINGS']['send1'])
            self.send2_entry.insert(END, config['SETTINGS']['send2'])
            self.send3_entry.insert(END, config['SETTINGS']['send3'])
        except:
            pass

    def get_ip_x(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def thread_function(self):
        while True:
            if not self.is_connect:
                del self.sock_server
                del self.sock_client
                break
            else:
                data, addr = self.sock_server.recvfrom(1024)
                self.received_text.insert(END, data)

    def connect(self):
        self.client_ip = self.client_ip_entry.get()
        self.client_port = self.client_port_entry.get()
        self.local_port = self.local_port_entry.get()

        try:
            self.sock_server.close()
        except:
            pass

        if not self.is_connect and self.client_ip and self.client_port and self.local_port:
            self.sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_server.bind((self.get_ip_x(), int(self.local_port_entry.get())))

            self.is_connect = True

            self.x = threading.Thread(target=self.thread_function, daemon=True)
            self.x.start()

            self.send1_button.configure(state=NORMAL)
            self.send2_button.configure(state=NORMAL)
            self.send3_button.configure(state=NORMAL)

            self.client_ip_entry.configure(state=DISABLED)
            self.client_port_entry.configure(state=DISABLED)
            self.local_port_entry.configure(state=DISABLED)

            self.connect_button['text'] = "Close"

        else:
            self.send1_button.configure(state=DISABLED)
            self.send2_button.configure(state=DISABLED)
            self.send3_button.configure(state=DISABLED)

            self.client_ip_entry.configure(state=NORMAL)
            self.client_port_entry.configure(state=NORMAL)
            self.local_port_entry.configure(state=NORMAL)

            self.is_connect = False
            self.connect_button['text'] = "Connect"

    def send_1(self):
        msg = self.send1_entry.get()
        if msg:
            self.sent_text.insert(END, msg)
            self.sock_server.sendto(bytes(msg, encoding='utf-8'), (
            bytes(self.client_ip_entry.get(), encoding='utf-8'), int(self.client_port_entry.get())))

    def send_2(self):
        msg = self.send2_entry.get()
        if msg:
            self.sent_text.insert(END, msg)
            self.sock_server.sendto(bytes(msg, encoding='utf-8'), (
            bytes(self.client_ip_entry.get(), encoding='utf-8'), int(self.client_port_entry.get())))

    def send_3(self):
        msg = self.send3_entry.get()
        if msg:
            self.sent_text.insert(END, msg)
            self.sock_server.sendto(bytes(msg, encoding='utf-8'), (
            bytes(self.client_ip_entry.get(), encoding='utf-8'), int(self.client_port_entry.get())))

    def on_closing(self):
        config = configparser.ConfigParser()
        config['SETTINGS'] = {}
        config['SETTINGS']['client_ip'] = self.client_ip
        config['SETTINGS']['client_port'] = self.client_port
        config['SETTINGS']['local_port'] = self.local_port
        config['SETTINGS']['send1'] = self.send1_entry.get()
        config['SETTINGS']['send2'] = self.send2_entry.get()
        config['SETTINGS']['send3'] = self.send3_entry.get()

        with open(self.cfg_file, 'w') as configfile:
            config.write(configfile)

        self.master.destroy()


def main():
    root = Tk()
    root.geometry("750x500+10+10")
    app = Window()
    root.mainloop()


if __name__ == '__main__':
    main()

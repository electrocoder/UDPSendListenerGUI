"""
electrocoder @ gmail.com
15.08.2019
"""
from tkinter import *
import time
import socket, struct, fcntl
import random
import logging
import threading


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.status = False
        self.create_widgets()
        self.close = False
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def thread_function(self):
        while True:
            if self.close:
                print("thread_function close")
                break
            else:
                print("thread_function recv")
                data = self.sock_server.recv(1024)
                self.receiver.insert(END, data)
                self.receiver.select_set(END, END)
                print("thread_function recv 1")

    def create_widgets(self):
        self.label1 = Label(self, text='Client IP')
        self.label1.grid(row=0, column=0)

        self.entry1 = Entry(self)
        self.entry1.grid(row=0, column=1)

        self.label2 = Label(self, text='Port')
        self.label2.grid(row=0, column=2)

        self.entry2 = Entry(self)
        self.entry2.grid(row=0, column=3)

        self.button1 = Button(self, text="Connect", command=self.connect)
        self.button1.grid(row=0, column=4)

        self.sendentry1 = Entry(self)
        self.sendentry1.grid(row=1, column=0)

        self.send1 = Button(self, text="Send 1", command=self.send_1)
        self.send1.grid(row=1, column=1)

        self.sendentry2 = Entry(self)
        self.sendentry2.grid(row=2, column=0)

        self.send2 = Button(self, text="Send 2", command=self.send_2)
        self.send2.grid(row=2, column=1)

        self.sendentry3 = Entry(self)
        self.sendentry3.grid(row=3, column=0)

        self.send3 = Button(self, text="Send 3", command=self.send_3)
        self.send3.grid(row=3, column=1)

        self.sb = Scrollbar(self, orient=VERTICAL)

        self.receiver = Listbox(self, exportselection=0, yscrollcommand=self.sb.set,
                               width=30, height=6, selectmode=SINGLE)
        self.receiver.grid (row=4, column=0, rowspan=4, columnspan=4, sticky=N+E+S+W)

        self.sb.config(command=self.receiver.yview)
        self.sb.grid(column=4, sticky=N+S)


        self.quit = Button(self, text="QUIT", fg="red",
                           command=self.master.destroy)
        self.quit.grid(row=8, column=0)

    def send_1(self):
        print("send 1")
        msg = "vvv"
        self.sock_client.sendto(bytes(msg, encoding='utf-8'), ("192.168.1.115", 3333))
        self.receiver.insert(END, msg)

    def send_2(self):
        print("send 2")
        msg = "q"
        self.sock_client.sendto(bytes(msg, encoding='utf-8'), ("192.168.1.115", 3333))
        self.receiver.insert(END, msg)

    def send_3(self):
        print("send 3")
        msg = "mmmmm"
        self.sock_client.sendto(bytes(msg, encoding='utf-8'), ("192.168.1.115", 3333))
        self.receiver.insert(END, msg)

    def connect(self):
        if not self.status:
            print("connect")
            self.sock_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock_server.bind(("192.168.1.126", 3333))
            self.button1['text'] = "Close"

            self.receiver.select_set(END, END)
            self.x = threading.Thread(target=self.thread_function)
            self.x.start()

            self.status=True
        else:
            print("close")
            self.status = False
            self.close = True
            self.button1['text'] = "Connect"

    def on_closing(self):
        print("on_closing")
        self.master.destroy()

root = Tk()
root.title("UDP Send Listener GUI")
root.geometry("800x500+10+10")
app = Application(master=root)
app.mainloop()

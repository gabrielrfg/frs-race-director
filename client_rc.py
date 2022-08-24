import queue
import sys
import tkinter
import socketio
import pyttsx3
from queue import Queue
from threading import Thread
import time
from tkinter import *
import sys
import os


def form(penalty):
    if not in_form.get():
        in_form.set(True)
        penalty_type.set(penalty)
        f2.tkraise()

def message_form():
    if not in_form.get():
        in_form.set(True)
        f3.tkraise()

def sc_form(penalty=""):
    if not in_form.get():
        in_form.set(True)
        penalty_type.set(penalty)
        f4.tkraise()
    

def send_penalty():
    send_message(f'{penalty_type.get()} ' + f'for car number {car_number.get()}' + (f" for {reason.get()}" if reason.get() else ""))
    cancel()

def send_sc_message():
    send_message(f'{penalty_type.get()}.  {f" {reason.get()}" if reason.get() else ""}')
    cancel()

def send_custom_message():
    send_message(reason.get())
    cancel()

def cancel():
    penalty_type.set("")
    car_number.set(0)
    reason.set("")
    in_form.set(False)
    f1.tkraise()

root = Tk()
root.title("FRS PENALTY BROADCAST TOOL")
# root.wm_attributes('-toolwindow', 'True')
root.resizable(False, False)

f4 = Frame(root, highlightbackground="gray", highlightthickness=5)
f4.grid(row=0, column=0, rowspan=3,columnspan=3, sticky='w')

f3 = Frame(root, highlightbackground="gray", highlightthickness=5)
f3.grid(row=0, column=0, rowspan=3,columnspan=3, sticky='w')

f2 = Frame(root, highlightbackground="gray", highlightthickness=5)
f2.grid(row=0, column=0, rowspan=3,columnspan=3, sticky='w')

f1 = Frame(root)
f1.grid(row=0, column=0, rowspan=3,columnspan=2, sticky='w')
f2.place(in_=f1, anchor="c", relx=.5, rely=.5)
f3.place(in_=f1, anchor="c", relx=.5, rely=.5)
f4.place(in_=f1, anchor="c", relx=.5, rely=.5)

reason = StringVar()
car_number = StringVar()
penalty_type = StringVar()
in_form = BooleanVar()


Button(f1,height = 9, width = 21,bg="lightsalmon", text = "Time Penalty", command=lambda:form("Time Penalty")).grid(row = 0, column = 0, sticky='we')
Button(f1,height = 9, width = 21,bg="lightcoral", text = "Stop and Go Penalty", command=lambda:form("Stop and Go Penalty")).grid(row = 0, column = 1, sticky='we')
Button(f1,height = 9, width = 21,bg="lightyellow", text = "Warning", command=lambda:form("Warning")).grid(row = 1, column = 0, sticky='we')
Button(f1,height = 9, width = 21,bg="orange", text = "Full Course Yellow", command=lambda:sc_form("Full Course Yellow")).grid(row = 1, column = 1, sticky='we')
Button(f1,height = 9, width = 21,bg="gold", text = "Safety Car", command=lambda:sc_form("Safety Car")).grid(row = 0, column = 2, sticky='we')
Button(f1,height = 9, width = 21,bg="gainsboro", text = "Broadcast Message", command=message_form).grid(row = 1, column = 2, sticky='we')
Label(f2, text = "Reason").grid(row = 0, column = 0, sticky='we')
Entry(f2, textvariable=reason).grid(row = 0, column = 1, sticky='we')
Label(f2,text = "Car Number").grid(row = 1, column = 0, sticky='we')
Entry(f2, textvariable=car_number).grid(row = 1, column = 1, sticky='we')
Button(f2,bg="green", text = "Send", command=send_penalty).grid(row = 2, column = 0, sticky='we')
Button(f2,bg="red", text = "Cancel", command=cancel).grid(row = 2, column = 1, sticky='we')

Label(f3, text = "Message").grid(row = 0, column = 0, sticky='we')
Entry(f3, textvariable=reason).grid(row = 0, column = 1, sticky='we')
Button(f3,bg="green", text = "Send", command=send_custom_message).grid(row = 1, column = 0, sticky='we')
Button(f3,bg="red", text = "Cancel", command=cancel).grid(row = 1, column = 1, sticky='we')

Label(f4, text = "Aditional Message").grid(row = 0, column = 0, sticky='we')
Entry(f4, textvariable=reason).grid(row = 0, column = 1, sticky='we')
Button(f4,bg="green", text = "Send", command=send_sc_message).grid(row = 1, column = 0, sticky='we')
Button(f4,bg="red", text = "Cancel", command=cancel).grid(row = 1, column = 1, sticky='we')

sio = socketio.Client()
secret = "secret"
enlisted = False

def send_message(message):
    sio.emit('message_race_control', message)

@sio.event
def connect():
    sio.emit('enlist_race_control', secret)

@sio.event
def disconnect():
    print("disconnect")
    os.kill(os.getpid(), 9)


@sio.on('enlist_race_control_response')
def enlist_race_control_response(message):
    if message == "success":
        print("enlisted")
        enlisted = True
    else:
        print("failed")
        root.destroy()
        sio.disconnect()


# sio.connect("https://dulcet-answer-360423.nw.r.appspot.com")
sio.connect("http://localhost:8080")
root.mainloop()
sio.disconnect()
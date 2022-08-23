import os
from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

#dict instance containing the car numbers as keys and the socket ids as values
# socket_dict = {}


@sio.on('register_number')
def register_number(sid, number):
    # car_number = int(number)
    # if car_number in socket_dict.keys():
    #     sio.emit('register_number_response', "Failure")
    # else:
    #     socket_dict[int(number)] = sid
    #     sio.emit('register_number_response', "Success")
    sio.emit('register_number_response', "Success")

@sio.on('message')
def print_message(sid, message):
    print(sid, message) 

@sio.event
async def connect(sid, environ, auth):
    #await sio.emit('message', "Drive through penalty for car number 69 420")
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

web.run_app(app, port=os.environ.get('PORT'))
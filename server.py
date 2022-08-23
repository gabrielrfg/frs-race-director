import os
from aiohttp import web
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('message')
def print_message(sid, message):
    print(sid, message) 

@sio.event
async def connect(sid, environ, auth):
    await sio.emit('message', "Drive through penalty for car number 69 420")
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)


web.run_app(app, port=os.environ.get('PORT'))
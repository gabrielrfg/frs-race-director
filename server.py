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
    await sio.emit('message', "HeLLo")
    print('connect ', sid)



web.run_app(app, port=os.environ.get('PORT'))
print("he he")
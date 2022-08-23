import os
from aiohttp import web
import socketio

secret = "secret"
sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)
race_control_sid = 0



@sio.on('enlist_race_control')
def enlist_race_control(sid, message):
    if race_control_sid == 0 and message == secret:
        race_control_sid = sid
        sio.emit('enlist_race_control_response', "success")
    else:
        sio.emit('enlist_race_control_response', "error")



@sio.on('message_race_control')
def handle_race_control_message(sid, message):
    sio.emit('message', message)

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    if sid == race_control_sid:
        race_control_sid = 0

web.run_app(app, port=os.environ.get('PORT'))
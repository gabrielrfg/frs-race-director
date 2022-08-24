import os
from aiohttp import web
import socketio



sio = socketio.AsyncServer()
app = web.Application()
state = {"secret" : "secret", "race_control_sid":0}
app["state"] = state
sio.attach(app)

@sio.on('enlist_race_control')
async def enlist_race_control(sid, message):
    if app["state"]["race_control_sid"] == 0 and message == app["state"]["secret"]:
        app["state"]["race_control_sid"] = sid
        await sio.emit('enlist_race_control_response', "success", sid)
    else:
        await sio.emit('enlist_race_control_response', "error", sid)



@sio.on('message_race_control')
async def handle_race_control_message(sid, message):
    await sio.emit('message', message)

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    print('disconnect ', sid)
    if sid == app["state"]["race_control_sid"]:
        app["state"]["race_control_sid"] = 0

web.run_app(app, port=os.environ.get('PORT'))
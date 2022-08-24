import os
from aiohttp import web
import socketio



sio = socketio.AsyncServer()
app = web.Application()
app["secret"] = "secret"
app["race_control_sid"] = 0
sio.attach(app)

def hello(a):
    return "hello"

app.add_routes([web.get('/', hello)])

@sio.on('enlist_race_control')
async def enlist_race_control(sid, message):
    print(app["race_control_sid"])
    if app["race_control_sid"] == 0 and message == app["secret"]:
        app["race_control_sid"] = sid
        await sio.emit('enlist_race_control_response', "success")
    else:
        await sio.emit('enlist_race_control_response', "error")



@sio.on('message_race_control')
async def handle_race_control_message(sid, message):
    print("rc")
    await sio.emit('message', message)

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)

@sio.event
async def disconnect(sid):
    if sid == app["race_control_sid"]:
        app["race_control_sid"] = 0

web.run_app(app, port=os.environ.get('PORT'))
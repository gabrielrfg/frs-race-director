import os
from aiohttp import web
import socketio
import jwt


sio = socketio.AsyncServer()
app = web.Application()
state = {"key": "key", "secret" : "secret", "race_control_sid":0}
app["state"] = state
sio.attach(app)

@sio.on('enlist_race_control')
async def enlist_race_control(sid, message):
    result = ""
    try:
        decoded = jwt.decode(message, app["state"]["key"], algorithms=["HS256"])["secret"]
        if decoded != app["state"]["secret"]:
            result = "Wrong Password"
        elif app["state"]["race_control_sid"] != 0:
            result = "Race Director already connected"
        else:
            result = "success"
    except jwt.exceptions.InvalidSignatureError:
        result = "Wrong Password"

    await sio.emit('enlist_race_control_response', result, sid)



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
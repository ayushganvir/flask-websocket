from hashlib import new
from logging import debug
from mimetypes import init
import uuid
from flask import *
from flask_socketio import *
import datetime, time
from threading import Lock
from dataclasses import dataclass
from typing import List, Set
from flask_session import Session


# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = '05bd39daf21d8c451717561784de548b'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# app.config['SESSION_COOKIE_SAMESITE'] = 'None'
# app.config['SESSION_COOKIE_SECURE'] = True
async_mode = None
socketio = SocketIO(app, logger=True, ping_interval=(2,1), async_mode=async_mode, manage_session=False)
thread = None
thread_lock = Lock()

number_of_clients = 0


class Client():

    def __init__(self, session, time_active):
        self.session = session
        self.time_active =time_active
        self.sid = set()
    
    def add_sid(self, sid):
        self.sid.add(sid)

    def remove_sid(self, sid):
        self.sid.remove(sid)
    
clients = set()

@app.route('/')
def hi(): 
    return render_template('connection.html', async_mode=socketio.async_mode)


def client_ping(t = 60):
    while True:
        socketio.sleep(t)
        date_time = datetime.datetime.now().strftime("%H:%M:%S")
        socketio.emit('minutely_message', {
            'message': 'Connected on time' + date_time + ' See you in a Minute'
    })
    

@socketio.on('connect')
def connect():
    socketio.start_background_task(client_ping)
    # emit('number_of_users', {'n': number_of_clients}, broadcast=True)
    print("Connect> ", session.sid, request.sid)


@socketio.on('disconnect')
def disconnect():
    # emit('number_of_users', {'n': number_of_clients}, broadcast=True)
    print("Disconnect")

@socketio.on('time_since')
def time_since():
    global clients
    for client in clients:
        if client.session == session.sid:
            c = time.time()
            active_time = round(c - client.time_active, 2)
            print('Active time is>>>>>', active_time)
            emit('set_time', {'time' : active_time})


@socketio.on("register")
def register():
    global Client, clients, number_of_clients
    print('In register')
    new_client = True
    for client in clients:
        if session.sid == client.session:
            print('New socked id added')
            emit('number_of_users', {'n': number_of_clients}, broadcast=True)

            client.add_sid(request.sid)
            new_client = False
            break
    if new_client:
        print('>>>>>>>>>', session.sid)
        number_of_clients += 1
        time_active = time.time()
        c = Client(session=session.sid ,time_active=time_active)
        c.add_sid(request.sid)
        clients.add(c)
        print([c.session for c in clients])
        emit('number_of_users', {'n': number_of_clients}, broadcast=True)

    

@socketio.on('deregister')
def remove_session():
    global clients, Client, number_of_clients
    for client in clients:
        if request.sid in client.sid:
            client.sid.remove(request.sid)
            print('Socket removed')
            if len(client.sid) == 0:
                clients.remove(client)
                print('session removed')
                number_of_clients -= 1
                print('removed')
                emit('number_of_users', {'n': number_of_clients}, broadcast=True)
                emit('remove_user')
                break


# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app, port=8000, debug=True)

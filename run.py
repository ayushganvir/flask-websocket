import uuid
from flask import *
from flask_socketio import *
import datetime, time
from threading import Lock


# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
async_mode = None
socketio = SocketIO(app, logger=True, ping_interval=(2,1), async_mode=async_mode)
thread = None
thread_lock = Lock()

clients = {}

@app.route('/')
def hi():  
    return render_template('connection.html', async_mode=socketio.async_mode)


def client_ping(t = 60):
    while True:
        socketio.sleep(t)
        date_time = datetime.datetime.now().strftime("%H:%M:%S")
        socketio.emit('minutely_message',
                      {'message': 'Connected on time' + date_time + ' See you in a Minute'})
    

@socketio.on('connect')
def connect():
    socketio.start_background_task(client_ping)
    print("Connect")


@socketio.on('disconnect')
def disconnect():
    print("Disconnect")
    pass

@socketio.on('time_since')
def time_since():
    global clients
    c = time.time()
    active_time = round(c - clients[request.sid], 2)
    print('Active time is>>>>>', active_time)
    emit('set_time', {'time' : active_time})


@socketio.on("register")
def register():
    global clients
    print("register sid:", request.sid)
    curr_time = time.time()
    clients[request.sid] = curr_time
    print('Number of clients>>>>>',len(clients))
    emit('number_of_users', {'n': len(clients)}, broadcast=True)
    

@socketio.on('deregister')
def remove_session():
    global clients
    print("disconnect sid", request.sid)
    clients.pop(request.sid)
    emit('number_of_users', {'n': len(clients)}, broadcast=True)
    emit('remove_user')

# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app, port=8000, debug=True)

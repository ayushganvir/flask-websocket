import uuid
from flask import *
from flask_socketio import *
import datetime, time
from datetime import timedelta


# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True, ping_interval=(2,1))
clients = {}

@app.route('/')
def hi():  
    return render_template('connection.html')

    

@socketio.on('connect')
def connect():
    print("Connect")


@socketio.on('disconnect')
def disconnect():
    print("Disconnect")
    pass

@socketio.on('time_since')
def time_since():
    global clients
    c = time.time()
    emit('set_time', {'time' : c - clients[request.sid]})


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

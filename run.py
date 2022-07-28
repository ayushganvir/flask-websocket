import uuid
from flask import *
from flask_socketio import *

# Init the server
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some super secret key!'
socketio = SocketIO(app, logger=True)

clients = set()


@app.route('/')
def hi():  
    return render_template('connection.html')

@socketio.on('connect')
def connect():
    print("connect sid:", request.sid)

@socketio.on("register")
def register(data):
    global clients
    print("register sid:", request.sid)
    clients.add(request.sid)
    # if not data.get('uuid'):
    #     uid = uuid.uuid4().hex
    #     emit("registered", {'uid': uid})
    #     clients.add(uid)
    # else:
    #     if data['uuid'] not in clients:
    #         clients.add(data['uuid'])
    emit('number_of_users', {'n': len(clients)}, broadcast=True)


@socketio.on('disconnect_user')
def remove_session(data):
    global clients
    print("disconnect sid", request.sid)
    clients.remove(request.sid)
    
def test_connect():
    print('>>>>>>> connected')
    emit('my response', {'data': 'Connected'})

def test_disconnect():
    print('Client disconnected')
# Receive a message from the front end HTML


@socketio.on('send_message')
def message_received(data):
    print(data['text'])
    emit('message_from_server', {'text': 'Message received!'})


# Actually Start the App
if __name__ == '__main__':
    """ Run the app. """
    socketio.run(app, port=8000, debug=True)

import uuid
from flask import *
from flask_socketio import *
from dataclasses import dataclass

@dataclass
class InventoryItem:
    name: str
    unit_price: float
    quantity_on_hand: int = 0



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
    print('>>> Session', Request, type(Request))
    global clients
    print("register sid:", request.sid)
    clients.add(request.sid)
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

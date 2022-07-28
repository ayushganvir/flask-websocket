# Flask websocket io 

## Websocket Implementation for basic understanding.

WebSocket is a protocol,that provides full-duplex communication channels over a single TCP connection.


### To install requirements for the project:
```python
pip install -r requirements.txt
```

Run  ```python run.py``` to start the server.
The port is 8000. Go to ```http://127.0.0.1:8000/``` to start a client instance.
The clients are distinguished by socket id (sid), so you don't need to open different browser sessions to make new clients. Every new tab instance is a different client.

### Features:

1. The server sends "Connected" message every 1-min to all the connected clients asynchronously.

2. Shows the total number of connected users.

3. Shows time since the client is connected.
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app)
@app.route('/')
def main():
    return render_template('home.j2')

@socketio.on('start_session')
def start_new_session(data):
    print('New session started', data)

    # We enjoy chaos. 10% of the time, send a session_start_failed event
    if random.random() < 0.10:
        emit('session_start_failed', {'clientId': data})
    else:
        emit('session_started', {'clientId': data, 'sessionId': data})

@socketio.on('send_message')
def handle_new_message_event(data):
    print('Received new message:', data)
    emit('broadcast_message', {'user': data['user'], 'message': data['message']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)

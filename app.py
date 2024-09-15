from pyexpat.errors import messages

from flask import Flask, session, request, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test'
socketio = SocketIO(app)

# Dictionary to map sessions to usernames
users = {}

@app.route('/')
def main():
    return render_template('home.j2')

@socketio.on('connect')
def handle_connect():
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    user = users.get(request.sid)
    room = session.get('room')

    if user and room:
        on_leave({'user': user, 'room': room})

    users.pop(request.sid, None)


@socketio.on('join')
def on_join(data):
    user = data['user']
    room = data['room']

    session['user'] = user
    session['room'] = room
    users[request.sid] = user

    join_room(room)
    emit('user_joined', {'user': user, 'room': room}, broadcast=True, to=room)

@socketio.on('leave')
def on_leave(data):
    user = data['user']
    room = data['room']

    leave_room(room)
    emit('broadcast', {'user': user, 'message': 'has left the chat.'}, broadcast=True, to=room)

@socketio.on('send_message')
def handle_new_message_event(data):
    user = data['user']
    room = data['room']
    message = data['message']

    emit('broadcast', {'user': user, 'message': message}, broadcast=True, to=room)

if __name__ == '__main__':
    socketio.run(app)

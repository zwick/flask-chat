import datetime

from flask import session, request, render_template
from flask_socketio import emit, join_room, leave_room
from app import app, socketio
from .messaging import Message, process_incoming_message
from .users import User, get_user_by_sid, sign_in_user, sign_out_user

@app.route('/')
def main():
    return render_template('home.j2')

@socketio.on('connect')
def handle_connect(auth):
    user = User(**{
        'sid': request.sid
    })
    sign_in_user(user)

    print(f"{user.username}/{user.sid} connected")
    emit('connected', {'data': 'Connected'})

@socketio.on('disconnect')
def handle_disconnect():
    user = get_user_by_sid(request.sid)
    room = session.get('room')

    if user and room:
        on_leave({'user': user.username, 'room': room})

    print(f"{user.username}/{user.sid} disconnected")
    sign_out_user(user)

@socketio.on('update_username')
def update_username(data):
    user = get_user_by_sid(request.sid)
    print(f"{user.username}/{request.sid} updated username to {data['username']}")

    user.username = data['username']
    user.save()

    emit('user_updated')

@socketio.on('join')
def on_join(data):
    user = get_user_by_sid(request.sid)
    room = data['room']
    print(f'{user.username} joined {room}')

    join_room(room)
    emit('user_joined', {'user': user.username, 'room': room}, broadcast=True, to=room)

@socketio.on('leave')
def on_leave(data):
    user = get_user_by_sid(request.sid)
    room = data['room']
    print(f'{user.username} left {room}')

    leave_room(room)
    emit('broadcast', {'user': user.username, 'message': 'has left the chat.'}, broadcast=True, to=room)

@socketio.on('send_message')
def handle_new_message_event(data):
    print(f"{request.sid} sent message to room: {data['room']}")
    message = Message(**{
        "sender": request.sid,
        "recipient": data['room'],
        "message": data['message'],
        "sent_timestamp": datetime.datetime.now().isoformat(),
    })
    process_incoming_message(message)

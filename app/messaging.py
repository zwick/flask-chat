import datetime

from .users import get_user_by_sid
from flask_socketio import emit
from redis_om import (
    JsonModel,
    Field
)

class Message(JsonModel):
    sender: str = Field(index=True)
    recipient: str = Field(index=True)
    message: str
    recipient_type: str = Field(default='room')
    sent_timestamp: datetime.datetime

def process_incoming_message(message: Message):
    message.save()
    username = get_user_by_sid(message.sender).username

    # TODO: Handle incoming messages for types other than "room". For now, we broadcast everything to the room.
    emit('broadcast', {'user': username, 'message': message.message}, broadcast=True, to=message.recipient)


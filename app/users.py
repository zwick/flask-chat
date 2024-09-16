from typing import Optional

from redis_om import (
    JsonModel,
    Field
)

class User(JsonModel):
    sid: str = Field(index=True)
    username: Optional[str] = Field(default='Anonymous')

def sign_in_user(user: User):
    user.save()

def sign_out_user(user: User):
    user.expire(0)

def get_active_users():
    return User.find().all()

def get_user_by_sid(sid: str):
    return User.find(User.sid == sid).first()


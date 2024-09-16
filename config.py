import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'never-leave-this-key-in-your-code'
    REDIS_OM_URL = os.environ.get('REDIS_OM_URL') or 'redis://localhost:6379'
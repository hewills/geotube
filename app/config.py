import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    VERSION = '1.5'
    MAP_KEY = 'YOUR GOOGLE MAP KEY'
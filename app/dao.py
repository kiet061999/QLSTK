from app import app, login
import hashlib
from flask_login import login_user
from app.models import *


def validate_user(username, password):
    return User.query.filter(User.username == username,
                             User.password == password).first()


def load(user_id):
    return User.query.get(user_id)

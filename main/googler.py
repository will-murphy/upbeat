
from google.appengine.api import users

def get_current_user():
    return users.get_current_user()

def nickname():
    return users.get_current_user().nickname()
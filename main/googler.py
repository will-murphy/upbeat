
def get_current_user():
    from google.appengine.api import users
    return users.get_current_user()

def nickname():
    return 'foo'
    from google.appengine.api import users as u
    return u.get_current_user().nickname()
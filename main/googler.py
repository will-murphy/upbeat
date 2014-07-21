
try:
    from google.appengine.api import users

    def get_current_user():
        return users.get_current_user()

    def nickname():
        return users.get_current_user().nickname()
    
    get_current_user()
    nickname()
except AssertionError:
    TEST_NAME = 'tennien'
    
    class Temp():
        def nickname():
            return TEST_NAME
    
    def get_current_user():
        return Temp()
    
    def nickname():
        return TEST_NAME

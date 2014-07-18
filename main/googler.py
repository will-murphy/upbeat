
try:
    from google.appengine.api import users
    user = users.get_current_user()
except AssertionError:
    print("Warning: I see no google.appengine.api, so I'll assume we're in " +
          "development and I'll create a fake user.")

    class Temp:
        def nickname(self):
            return 'iamatest'

    user = Temp()
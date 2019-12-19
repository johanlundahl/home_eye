
class User:

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def authenticate(self, password):
        return self.password == password

    def authorize(self, access_level):
        return True #self.access_level >= access_level

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return 1
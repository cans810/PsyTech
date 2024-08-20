from handlers.RegistrationHandler import RegistrationHandler
from handlers.LoginHandler import LoginHandler

class AuthHandler:
    def __init__(self, db, users_ref):
        self.registration_handler = RegistrationHandler(db, users_ref)
        self.login_handler = LoginHandler(db, users_ref)

    def register_user(self, email, password):
        return self.registration_handler.register_user(email, password)

    def login_user(self, email, password):
        return self.login_handler.login_user(email, password)


class LoginHandler:
    def __init__(self, db, users_ref):
        self.db = db
        self.users_ref = users_ref

    def login_user(self, email, password):
        if not email or not password:
            return "Email and password are required."

        user_data = self.get_user_by_email(email)
        if user_data:
            stored_password = user_data.get('password')
            if stored_password == password:
                return "Login successful."
            else:
                return "Invalid password."
        else:
            return f"No user found with the email {email}"

    def get_user_by_email(self, email):
        # Check if the user exists by email
        user_ref = self.users_ref.document(email)
        user_doc = user_ref.get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            return None

import re

class RegistrationHandler:
    def __init__(self, db, users_ref):
        self.db = db
        self.users_ref = users_ref

    def is_valid_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email)

    def is_valid_password(self, password):
        return 8 <= len(password) <= 16

    def register_user(self, email, password):
        if not email or not password:
            return "Email and password are required."

        if not self.is_valid_email(email):
            return "Invalid email format. Please enter a valid email address."

        if not self.is_valid_password(password):
            return "Invalid password. Password should be at least 8 characters long."

        # Check if the user already exists
        if self.get_user_by_email(email):
            return "User already exists with this email."

        # Add the user to Firebase Firestore
        self.users_ref.document(email).set({
            'email': email,
            'password': password,
            'reset_token': None,
            'token_generated_at': None,
            'patients': []  # initialize an empty list for patients associated with this specialist
        })

        return "Registration successful!"

    def get_user_by_email(self, email):
        # Check if the user exists by email
        user_ref = self.users_ref.document(email)
        user_doc = user_ref.get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            return None

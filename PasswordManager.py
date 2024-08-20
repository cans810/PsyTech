import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from datetime import datetime


class PasswordChangeManager:
    def __init__(self, db, users_ref):
        self.db = db
        self.users_ref = users_ref

    def generate_token(self, email, length=8):
        characters = string.ascii_letters + string.digits
        token = ''.join(random.choice(characters) for _ in range(length))

        # reset token generate ediliyor ve edildiği saat de ilgili hesabın firebaseinde update ediliyor
        try:
            self.users_ref.document(email).update({
                'reset_token': token,
                'token_generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            })
        except Exception as e:
            print(f"Error occurred while updating token generated time: {e}")

        return token
    
    def change_password(self, user_email, new_password):
        try:
            # Find the user document in the database
            user_query = self.users_ref.where('email', '==', user_email).limit(1).get()
            if user_query:
                user_doc = user_query[0]
                # Update the user's password in the database
                user_doc.reference.update({'password': new_password})
                return True, "Password changed successfully."
            else:
                return False, "User not found."
        except Exception as e:
            return False, f"An error occurred: {e}"

    def reset_token_expiry(self, user_ref):
        try:
            # ensure user_ref is a valid document reference
            if user_ref:
                # iterate over the documents in the list (should be only one document)
                for doc in user_ref:
                    # update the reset_token and token_generated_at fields
                    doc.reference.update({'reset_token': None, 'token_generated_at': None})
        except Exception as e:
            print(f"Error occurred while resetting token: {e}")

    def is_token_expired(self, token_generated_at):
        try:
            if token_generated_at:
                if isinstance(token_generated_at, list):
                    # if token_generated_at is a list, take the first element as the string representation
                    token_generated_at = token_generated_at[0].to_dict().get('token_generated_at')

                # parse the datetime string into a datetime object
                token_generated_datetime = datetime.strptime(token_generated_at, '%Y-%m-%d %H:%M:%S.%f')
                # calculate the difference between the current time and the token generation time
                time_difference = datetime.now() - token_generated_datetime
                # check if the token has expired (e.g., 10 minutes)
                return time_difference.total_seconds() > 600  # 600 seconds = 10 minutes
            else:
                # token is considered expired if it's not generated yet
                return True
        except Exception as e:
            print(f"Error occurred while checking token expiry: {e}")
            return True  # treat as expired if there's an error




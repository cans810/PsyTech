from flask import Flask, request
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

# Firebase Admin SDK'nın başlatılması
cred = credentials.Certificate("C:\\Users\\Can\\Desktop\\PsyTech-side1\\PrivateKeyNew\\psytech-daab2-firebase-adminsdk-cchk5-f651b0241b.json")  # Firebase Service Account Key'inizin yolu
firebase_admin.initialize_app(cred)

# Kullanıcı erişimini kontrol etme
@app.route('/protected-route')
def protected_route():
    token = request.headers.get('Authorization').split(' ')[1]
    try:
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        # Kullanıcının erişim kontrolü
        # Örneğin, Firebase Realtime Database'de belirli bir yol için erişim kontrolü yapabilirsiniz.
        # Veri tabanınızı önceden yapılandırmanız gerekebilir.

        return "Access granted! User ID: " + uid
    except auth.InvalidIdTokenError:
        return "Invalid ID token"
    except auth.ExpiredIdTokenError:
        return "Expired ID token"
    except auth.RevokedIdTokenError:
        return "Revoked ID token"

if __name__ == '__main__':
    app.run(debug=True)

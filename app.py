from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from flask_mail import Mail, Message
import os
from firebase_admin import credentials, firestore
from Graphs import GraphsManager
from handlers.AuthHandler import AuthHandler
from PasswordManager import PasswordChangeManager
from handlers.RegistrationHandler import RegistrationHandler
from PatientManager import PatientManager
from datetime import datetime
from handlers.TestsHandler import TestsHandler
import json
import Functions
import base64

# Test merge stuff

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "your_secret_key"  # You should provide a strong secret key here

# Initialize Firebase Admin SDK


cred = credentials.Certificate("C:\\Users\\Can\\Documents\\GitHub\\PsyTech\\PrivateKeyNew\\psytech-daab2-firebase-adminsdk-cchk5-f651b0241b.json")


firebase_admin.initialize_app(cred)
db = firestore.client()
users_ref = db.collection('users')
answers_ref = db.collection('answers')

auth_handler = AuthHandler(db, users_ref)
password_manager = PasswordChangeManager(db, users_ref)
patient_manager = PatientManager(db, users_ref, answers_ref)
tests_handler = TestsHandler(db, users_ref)
graphs_manager = GraphsManager(db, answers_ref)

# Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'psytechtr@gmail.com'  # Your Gmail email address
app.config['MAIL_PASSWORD'] = 'jaut wvbc bapx lbtp'  # Your Gmail password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initialize Mail instance
mail = Mail(app)


# @app.route() -> down below
# Add appointment
# Remove appointment
# Edit appointment


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/profile')
def self_profile():
    if 'user_email' in session:
        user_email = session['user_email']
        user_data = get_user_data(user_email)
        if user_data:
            user_password = user_data.get('password')
            return render_template('self_profile.html', user_email=user_email, user_password=user_password)
        else:
            return "User data not found"
    else:
        return redirect(url_for('login'))


@app.route('/main_page')
def main_page():
    if 'user_email' in session:
        user_email = session['user_email']
        return render_template('main_page.html', user_email=user_email)
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = auth_handler.login_user(email, password)
        if result == "Login successful.":
            session['user_email'] = email
            return redirect(url_for('main_page'))
        else:
            return result
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        result = auth_handler.register_user(email, password)
        if result == "Registration successful!":
            session['user_email'] = email
            return redirect(url_for('main_page'))
        else:
            return result
    else:
        return render_template('registration.html')


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('login'))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        email = session.get('user_email')
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        # Check if the old password provided by the user matches the current password
        if auth_handler.login_user(email, old_password) == "Login successful.":
            # Change the password
            password_manager.change_password(email, new_password)
            return redirect(url_for('main_page'))
        else:
            return "Old password is incorrect. Please try again."
    else:
        return render_template('change_password.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        token = password_manager.generate_token(email)
        try:
            user_ref = users_ref.where('email', '==', email).limit(1).get()
            if user_ref:
                password_reset_link = url_for('reset_password', token=token, _external=True)

                # Send the email
                msg = Message('Password Reset', sender='your_email@gmail.com', recipients=[email])
                msg.body = f'Click the following link to reset your password: {password_reset_link}'
                mail.send(msg)

                return redirect(url_for('sent_password_recovery'))
            else:
                return "User not found"
        except Exception as e:
            return f"Error occurred while sending reset email: {e}"
    else:
        return render_template('enter_email_to_change_password.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        new_password = request.form['new_password']
        token = request.form['token']
        registration_handler = RegistrationHandler(db, users_ref)
        if not registration_handler.is_valid_password(new_password):
            return "Invalid password. Password must be between 8 and 16 characters long."
        user_ref = users_ref.where('reset_token', '==', token).limit(1).get()
        if user_ref:
            if password_manager.is_token_expired(user_ref):
                return "Invalid or expired token"
            try:
                user_ref[0].reference.update({'password': new_password})
                password_manager.reset_token_expiry(user_ref)
                return redirect(url_for('reset_password_success'))
            except Exception as e:
                return f"Error occurred while updating password: {e}"
        else:
            return "Invalid or expired token"
    else:
        token = request.args.get('token')
        if token:
            user_ref = users_ref.where('reset_token', '==', token).limit(1).get()
            if user_ref:
                if password_manager.is_token_expired(user_ref):
                    return "Invalid or expired token"
                return render_template('reset_password.html', token=token)
            else:
                return "Invalid or expired token"
        else:
            return "Invalid or expired token"


@app.route('/sent_password_recovery')
def sent_password_recovery():
    return render_template('sent_password_recovery.html')


@app.route('/reset_password_success')
def reset_password_success():
    return render_template('reset_password_success.html')


def get_user_data(user_email):
    query = users_ref.where('email', '==', user_email).limit(1)
    result = query.get()
    if result:
        for doc in result:
            user_data = doc.to_dict()
            return user_data
    return None


@app.route('/patients')
def patients():
    specialist_email = session.get('user_email')
    patients = patient_manager.get_patients_for_specialist(specialist_email)
    return render_template('patients.html', patients=patients)


@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        patient_name = request.form['patient_name']
        gender = request.form['gender']
        birthday = request.form['birthday']
        specialist_email = session.get('user_email')
        patient_manager.save_patient_data(specialist_email, patient_name, gender, birthday, "", "Bitmedi", 0)
        return redirect(url_for('patients'))
    else:
        return render_template('add_patient.html')


@app.route('/remove_patient/<patient_id>', methods=['POST'])
def remove_patient(patient_id):
    specialist_email = session.get('user_email')
    patient_manager.remove_patient(specialist_email, patient_id)
    return redirect(url_for('patients'))


@app.route('/enter_test_info_popup/<patient_id>')
def enter_test_info_popup(patient_id):
    specialist_email = session.get('user_email')
    patient = patient_manager.find_patient_by_id(specialist_email, patient_id)
    if patient.get('current_test_assigned') not in ("", None):
        return "A test link is already assigned to this patient."
    return render_template('enter_test_info_popup.html', patient=patient)


@app.route('/create_test/<patient_id>', methods=['GET', 'POST'])
def create_test(patient_id):
    specialist_email = session.get('user_email')
    test_id = patient_manager.get_test_id(specialist_email, patient_id)
    if request.method == 'POST':
        due_date = request.form.get('dueDate')
        due_hour = request.form.get('dueHour')
        if not test_id:
            test_id = patient_manager.generate_unique_test_id()
        generated_test_link = f"http://127.0.0.1:5000/take_test/{test_id}"
        patient_manager.assign_test(specialist_email, patient_id, generated_test_link, "Bitmedi", due_date, due_hour,
                                    test_id, 0)
        return render_template('show_test_link.html', test_link=generated_test_link)
    return render_template('create_test.html', patient_id=patient_id)


@app.route('/remove_test_link/<patient_id>', methods=['POST'])
def remove_test_link(patient_id):
    # retrieve specialist email from session
    specialist_email = session.get('user_email')

    patient_manager.remove_test_link(specialist_email, patient_id)

    return redirect(url_for('patients'))


@app.route('/take_test/<test_id>', methods=['GET', 'POST'])
def take_test(test_id):
    if request.method == 'GET':
        due_date, due_hour = fetch_test_dueDate(test_id)
        if due_date and due_hour:
            due_date_time = datetime.strptime(f"{due_date} {due_hour}", "%Y-%m-%d %H:%M")
            if due_date_time < datetime.now():
                return "Due time has passed. You cannot take the test."
            else:
                return render_template('Kvkk.html', test_id=test_id)
        else:
            return "Due date and time not found in test data."
    elif request.method == 'POST':
        if request.form.get('accept_terms') == 'yes':
            return redirect(url_for('show_questions', test_id=test_id))
        else:
            return "Please accept the terms to proceed."


@app.route('/show_questions/<test_id>')
def show_questions(test_id):
    due_date, due_hour = fetch_test_dueDate(test_id)

    if due_date and due_hour:
        due_date_time = datetime.strptime(f"{due_date} {due_hour}", "%Y-%m-%d %H:%M")
        if due_date_time < datetime.now():
            return "Due time has passed. You cannot take the test."
        else:
            questions = tests_handler.get_fixed_questions()
            saved_patient_answers = patient_manager.get_answers_by_test_id(test_id)
            elapsedTime = patient_manager.get_patient_elapsedTime(test_id)

            print(saved_patient_answers)
            print(elapsedTime, " elapsed time")

            return render_template('questionsPage.html', questions=questions, test_id=test_id,
                                   patient_answers=saved_patient_answers, elapsed_time=elapsedTime)
    else:
        return "Due date and time not found in test data."


@app.route('/submit_test', methods=['POST'])
def submit_test():
    try:
        # extract data from the JSON request
        test_data = request.json
        test_id = test_data.get('test_id')
        selected_options = test_data.get('answers', [])  # get all selected answers from the JSON payload
        time_elapsed = test_data.get('elapsedTime')

        # fetch all specialists
        all_specialists = users_ref.stream()

        for specialist_ref in all_specialists:
            specialist_data = specialist_ref.to_dict()
            patients = specialist_data.get('patients', [])

            for i, p in enumerate(patients):
                if p.get('test_id') == test_id:
                    specialist_doc = specialist_ref.reference
                    patients[i]['finished_current_test'] = "Bitti"
                    patients[i]['time_elapsed'] = time_elapsed
                    specialist_doc.update({'patients': patients})  # save the change back to Firestore
                    break

        # convert selected options to the desired format
        formatted_answers = []
        for option in selected_options:
            if option == "Doğru":
                formatted_answers.append("Doğru")
            elif option == "Yanlış":
                formatted_answers.append("Yanlış")
            elif option == "Boş":
                formatted_answers.append("Boş")

        # check if a document with the given test_id already exists
        answers_existing_doc = answers_ref.where('test_id', '==', test_id).limit(1).get()

        if answers_existing_doc:
            # update the existing document with the new answers
            for doc in answers_existing_doc:
                doc_ref = doc.reference
                doc_ref.update({'answers': formatted_answers})
        else:
            # create a document to store the answers
            answer_doc = {
                'test_id': test_id,
                'answers': formatted_answers,
                'finished': "Bitti",
                'generated_graph': None
            }
            # add the answers document to the Firestore collection
            answers_ref.add(answer_doc)

        return 'Test sonuçları kaydedildi.'
    except Exception as e:
        print(str(e))
        return 'Test sonuçlarını kaydedilirken bir hata oluştu.', 500


@app.route('/save_test', methods=['POST'])
def save_test():
    try:
        # extract data from the JSON request
        test_data = request.json
        test_id = test_data.get('test_id')
        selected_options = test_data.get('answers', [])  # get all selected answers from the JSON payload
        time_elapsed = test_data.get('elapsedTime')

        # fetch all specialists
        all_specialists = users_ref.stream()

        for specialist_ref in all_specialists:
            specialist_data = specialist_ref.to_dict()
            patients = specialist_data.get('patients', [])

            for i, p in enumerate(patients):
                if p.get('test_id') == test_id:
                    specialist_doc = specialist_ref.reference
                    patients[i]['time_elapsed'] = time_elapsed
                    # print(p.get('time_elapsed'), " is the time elapsed")
                    specialist_doc.update({'patients': patients})  # save the change back to Firestore
                    break

        # convert selected options to the desired format
        formatted_answers = []
        for option in selected_options:
            if option == "Doğru":
                formatted_answers.append("Doğru")
            elif option == "Yanlış":
                formatted_answers.append("Yanlış")
            elif option == "Boş":
                formatted_answers.append("Boş")

        # check if a document with the given test_id already exists
        answers_existing_doc = answers_ref.where('test_id', '==', test_id).limit(1).get()

        if answers_existing_doc:
            # update the existing document with the new answers
            for doc in answers_existing_doc:
                doc_ref = doc.reference
                doc_ref.update({'answers': formatted_answers})
        else:
            # create a document to store the answers
            answer_doc = {
                'test_id': test_id,
                'answers': formatted_answers,
                'finished': False,
                'generated_graph': None
            }
            # add the answers document to the Firestore collection
            answers_ref.add(answer_doc)

        return 'Test sonuçları kaydedildi.'
    except Exception as e:
        print(str(e))
        return 'Test sonuçlarını kaydedilirken bir hata oluştu.', 500


def get_due_date_time(test_data):
    # check if test_data contains the due date and time
    if 'due_date' in test_data and 'due_hour' in test_data:
        # Extract due date and time components
        due_date = test_data['due_date']
        due_hour = test_data['due_hour']

        # combine due date and time into a single string
        due_date_time_str = f"{due_date} {due_hour}"

        # convert due date and time string to a datetime object
        due_date_time = datetime.strptime(due_date_time_str, '%Y-%m-%d %H:%M:%S')

        return due_date_time

    else:
        return None


def fetch_test_dueDate(test_id):
    try:
        for user_ref in users_ref.stream():
            user_data = user_ref.to_dict()
            patients = user_data.get('patients', [])
            for patient in patients:
                if patient.get('test_id') == test_id:
                    return patient.get('due_date'), patient.get('due_hour')
    except Exception as e:
        print(f"Error fetching test data: {e}")
        return None, None


@app.route('/see_test_results/<patient_id>', methods=['GET', 'POST'])
def see_test_results(patient_id):
    if request.method == 'POST':
        pass

        # logic to fetch and display test results for the given patient_id
        if patient_manager.get_patient_gender(patient_id) == "male":
            patient_answers = patient_manager.get_patient_answers(patient_id, answers_ref)
            patient_name = patient_manager.get_patient_name(patient_id)

            patient_gender = patient_manager.get_patient_gender(patient_id)


            patient_age = patient_manager.get_patient_age(patient_id)

            user_email = session['user_email']
            test_id = patient_manager.get_test_id(user_email, patient_id)

            empty_question_count = Functions.Bilmiyorum_Alt_Olcek(patient_answers)
            hampuan_L_Alt, L_Alt_Olcek = Functions.Erkek_L_Alt_Olcek(patient_answers)
            hampuan_F_Alt, F_Alt_Olcek = Functions.Erkek_F_Alt_Olcek(patient_answers)
            hampuan_K_Alt, K_Alt_Olcek = Functions.Erkek_K_Alt_Olcek(patient_answers)
            hampuan_Hs_Alt, Hs_Alt_Olcek = Functions.Erkek_Hs_Alt_Olcek(patient_answers)
            hampuan_D_Alt, D_Alt_Olcek = Functions.Erkek_D_Alt_Olcek(patient_answers)
            hampuan_Hy_Alt, Hy_Alt_Olcek = Functions.Erkek_Hy_Alt_Olcek(patient_answers)
            hampuan_Pd_Alt, Pd_Alt_Olcek = Functions.Erkek_Pd_Alt_Olcek(patient_answers)
            hampuan_Mf_Alt, Mf_Alt_Olcek = Functions.Erkek_Mf_Alt_Olcek(patient_answers)
            hampuan_Pa_Alt, Pa_Alt_Olcek = Functions.Erkek_Pa_Alt_Olcek(patient_answers)
            hampuan_Pt_Alt, Pt_Alt_Olcek = Functions.Erkek_Pt_Alt_Olcek(patient_answers)
            hampuan_Sc_Alt, Sc_Alt_Olcek = Functions.Erkek_Sc_Alt_Olcek(patient_answers)
            hampuan_Ma_Alt, Ma_Alt_Olcek = Functions.Erkek_Ma_Alt_Olcek(patient_answers)
            hampuan_Si_Alt, Si_Alt_Olcek = Functions.Erkek_Si_Alt_Olcek(patient_answers)

            graph = graphs_manager.generate_graph_and_save(test_id, empty_question_count, L_Alt_Olcek, F_Alt_Olcek,
                                                           K_Alt_Olcek, Hs_Alt_Olcek, D_Alt_Olcek, Hy_Alt_Olcek,
                                                           Pd_Alt_Olcek, Mf_Alt_Olcek, Pa_Alt_Olcek, Pt_Alt_Olcek,
                                                           Sc_Alt_Olcek, Ma_Alt_Olcek, Si_Alt_Olcek)

            graph = graphs_manager.generate_graph_and_save(test_id,empty_question_count,L_Alt_Olcek,F_Alt_Olcek,K_Alt_Olcek,Hs_Alt_Olcek,D_Alt_Olcek,Hy_Alt_Olcek,Pd_Alt_Olcek,Mf_Alt_Olcek,Pa_Alt_Olcek,Pt_Alt_Olcek,Sc_Alt_Olcek,Ma_Alt_Olcek,Si_Alt_Olcek)

            # retrieve encoded graph data from Firestore
            graph_base64 = None
            try:
                # Iterate through answer documents in answers_ref
                for answer_doc in answers_ref.stream():
                    answer_data = answer_doc.to_dict()

                    # Check if the test_id matches the patient's test_id
                    if answer_data.get('test_id') == test_id:
                        # Get the generated_graph if a match is found
                        graph_base64 = answer_data.get('generated_graph')
                        break
            except Exception as e:
                print(f"Error occurred while retrieving generated graph: {e}")

            return render_template(
                'testResultsPage.html',
                patient_id=patient_id,
                patient_name=patient_name,
                patient_age=patient_age,

                patient_gender=patient_gender,

                empty_question_count=empty_question_count,
                hampuan_L_Alt=hampuan_L_Alt,
                L_Alt_Olcek=L_Alt_Olcek,
                hampuan_F_Alt=hampuan_F_Alt,
                F_Alt_Olcek=F_Alt_Olcek,
                hampuan_K_Alt=hampuan_K_Alt,
                K_Alt_Olcek=K_Alt_Olcek,
                hampuan_Hs_Alt=hampuan_Hs_Alt,
                Hs_Alt_Olcek=Hs_Alt_Olcek,
                hampuan_D_Alt=hampuan_D_Alt,
                D_Alt_Olcek=D_Alt_Olcek,
                hampuan_Hy_Alt=hampuan_Hy_Alt,
                Hy_Alt_Olcek=Hy_Alt_Olcek,
                hampuan_Pd_Alt=hampuan_Pd_Alt,
                Pd_Alt_Olcek=Pd_Alt_Olcek,
                hampuan_Mf_Alt=hampuan_Mf_Alt,
                Mf_Alt_Olcek=Mf_Alt_Olcek,
                hampuan_Pa_Alt=hampuan_Pa_Alt,
                Pa_Alt_Olcek=Pa_Alt_Olcek,
                hampuan_Pt_Alt=hampuan_Pt_Alt,
                Pt_Alt_Olcek=Pt_Alt_Olcek,
                hampuan_Sc_Alt=hampuan_Sc_Alt,
                Sc_Alt_Olcek=Sc_Alt_Olcek,
                hampuan_Ma_Alt=hampuan_Ma_Alt,
                Ma_Alt_Olcek=Ma_Alt_Olcek,
                hampuan_Si_Alt=hampuan_Si_Alt,
                Si_Alt_Olcek=Si_Alt_Olcek,
                graph_base64=graph_base64
            )
        elif patient_manager.get_patient_gender(patient_id) == "female":
            patient_answers = patient_manager.get_patient_answers(patient_id, answers_ref)
            patient_name = patient_manager.get_patient_name(patient_id)

            patient_gender = patient_manager.get_patient_gender(patient_id)

            patient_age = patient_manager.get_patient_age(patient_id)

            user_email = session['user_email']
            test_id = patient_manager.get_test_id(user_email, patient_id)

            empty_question_count = Functions.Bilmiyorum_Alt_Olcek(patient_answers)
            hampuan_L_Alt, L_Alt_Olcek = Functions.Kadin_L_Alt_Olcek(patient_answers)
            hampuan_F_Alt, F_Alt_Olcek = Functions.Kadin_F_Alt_Olcek(patient_answers)
            hampuan_K_Alt, K_Alt_Olcek = Functions.Kadin_K_Alt_Olcek(patient_answers)
            hampuan_Hs_Alt, Hs_Alt_Olcek = Functions.Kadin_Hs_Alt_Olcek(patient_answers)
            hampuan_D_Alt, D_Alt_Olcek = Functions.Kadin_D_Alt_Olcek(patient_answers)
            hampuan_Hy_Alt, Hy_Alt_Olcek = Functions.Kadin_Hy_Alt_Olcek(patient_answers)
            hampuan_Pd_Alt, Pd_Alt_Olcek = Functions.Kadin_Pd_Alt_Olcek(patient_answers)
            hampuan_Mf_Alt, Mf_Alt_Olcek = Functions.Kadin_Mf_Alt_Olcek(patient_answers)
            hampuan_Pa_Alt, Pa_Alt_Olcek = Functions.Kadin_Pa_Alt_Olcek(patient_answers)
            hampuan_Pt_Alt, Pt_Alt_Olcek = Functions.Kadin_Pt_Alt_Olcek(patient_answers)
            hampuan_Sc_Alt, Sc_Alt_Olcek = Functions.Kadin_Sc_Alt_Olcek(patient_answers)
            hampuan_Ma_Alt, Ma_Alt_Olcek = Functions.Kadin_Ma_Alt_Olcek(patient_answers)
            hampuan_Si_Alt, Si_Alt_Olcek = Functions.Kadin_Si_Alt_Olcek(patient_answers)

            graph = graphs_manager.generate_graph_and_save(test_id, empty_question_count, L_Alt_Olcek, F_Alt_Olcek,
                                                           K_Alt_Olcek, Hs_Alt_Olcek, D_Alt_Olcek, Hy_Alt_Olcek,
                                                           Pd_Alt_Olcek, Mf_Alt_Olcek, Pa_Alt_Olcek, Pt_Alt_Olcek,
                                                           Sc_Alt_Olcek, Ma_Alt_Olcek, Si_Alt_Olcek)

            graph = graphs_manager.generate_graph_and_save(test_id,empty_question_count,L_Alt_Olcek,F_Alt_Olcek,K_Alt_Olcek,Hs_Alt_Olcek,D_Alt_Olcek,Hy_Alt_Olcek,Pd_Alt_Olcek,Mf_Alt_Olcek,Pa_Alt_Olcek,Pt_Alt_Olcek,Sc_Alt_Olcek,Ma_Alt_Olcek,Si_Alt_Olcek)

            # retrieve encoded graph data from Firestore
            graph_base64 = None
            try:
                # Iterate through answer documents in answers_ref
                for answer_doc in answers_ref.stream():
                    answer_data = answer_doc.to_dict()

                    # Check if the test_id matches the patient's test_id
                    if answer_data.get('test_id') == test_id:
                        # Get the generated_graph if a match is found
                        graph_base64 = answer_data.get('generated_graph')
                        break
            except Exception as e:
                print(f"Error occurred while retrieving generated graph: {e}")

            return render_template(
                'testResultsPage.html',
                patient_id=patient_id,
                patient_name=patient_name,
                patient_age=patient_age,

                patient_gender=patient_gender,


                empty_question_count=empty_question_count,
                hampuan_L_Alt=hampuan_L_Alt,
                L_Alt_Olcek=L_Alt_Olcek,
                hampuan_F_Alt=hampuan_F_Alt,
                F_Alt_Olcek=F_Alt_Olcek,
                hampuan_K_Alt=hampuan_K_Alt,
                K_Alt_Olcek=K_Alt_Olcek,
                hampuan_Hs_Alt=hampuan_Hs_Alt,
                Hs_Alt_Olcek=Hs_Alt_Olcek,
                hampuan_D_Alt=hampuan_D_Alt,
                D_Alt_Olcek=D_Alt_Olcek,
                hampuan_Hy_Alt=hampuan_Hy_Alt,
                Hy_Alt_Olcek=Hy_Alt_Olcek,
                hampuan_Pd_Alt=hampuan_Pd_Alt,
                Pd_Alt_Olcek=Pd_Alt_Olcek,
                hampuan_Mf_Alt=hampuan_Mf_Alt,
                Mf_Alt_Olcek=Mf_Alt_Olcek,
                hampuan_Pa_Alt=hampuan_Pa_Alt,
                Pa_Alt_Olcek=Pa_Alt_Olcek,
                hampuan_Pt_Alt=hampuan_Pt_Alt,
                Pt_Alt_Olcek=Pt_Alt_Olcek,
                hampuan_Sc_Alt=hampuan_Sc_Alt,
                Sc_Alt_Olcek=Sc_Alt_Olcek,
                hampuan_Ma_Alt=hampuan_Ma_Alt,
                Ma_Alt_Olcek=Ma_Alt_Olcek,
                hampuan_Si_Alt=hampuan_Si_Alt,
                Si_Alt_Olcek=Si_Alt_Olcek,
                graph_base64=graph_base64
            )

    return render_template('testResultsPage.html', patient_id=patient_id)


if __name__ == '__main__':
    app.run(debug=True)

import random
import string
from google.cloud.firestore_v1 import ArrayUnion
from datetime import datetime


class PatientManager:
    def __init__(self, db, users_ref, answers_ref):
        self.db = db
        self.users_ref = users_ref
        self.answers_ref = answers_ref

    def get_patients_for_specialist(self, specialist_email):
        patients = []
        try:
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_data = specialist_ref[0].to_dict()
                patients = specialist_data.get('patients', [])  # get patient data directly from the specialist's 'users' document

        except Exception as e:
            print(f"Error occurred while fetching patients: {e}")

        return patients

    def save_patient_data(self, specialist_email, patient_name, gender, birthday, current_test_assigned, finished_current_test, time_elapsed, due_date="", due_hour="" , test_id=""):
        try:
            # get the specialist document reference
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_doc = specialist_ref[0].reference

                # generate a unique patient ID
                patient_id = self.generate_unique_patient_id()

                # update the 'patients' field in the specialist's document with the new patient data
                new_patient_data = {
                    'id': patient_id,
                    'name': patient_name,
                    'gender': gender,
                    'birthday': birthday,
                    'current_test_assigned': current_test_assigned,
                    'finished_current_test': finished_current_test,
                    'due_date': due_date,
                    'due_hour': due_hour,
                    'test_id': test_id,
                    'time_elapsed': time_elapsed,
                }

                specialist_doc.update({'patients': ArrayUnion([new_patient_data])})

                print("Patient data saved successfully.")
            else:
                print("Specialist not found.")

        except Exception as e:
            print(f"Error occurred while saving patient data: {e}")

    def remove_patient(self, specialist_email, patient_id):
        try:
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_doc = specialist_ref[0].reference

                # get the current list of patients
                specialist_data = specialist_ref[0].to_dict()
                patients = specialist_data.get('patients', [])

                # if there's only one patient left, clear the patients list instead of removing the single patient
                if len(patients) == 1:
                    updated_patients = []
                else:
                    # iterate through patients list and remove the patient element that has the matching ID
                    updated_patients = [patient for patient in patients if patient.get('id') != patient_id]

                # update the 'patients' array field in the specialist's document
                specialist_doc.update({'patients': updated_patients})

                print("Patient removed successfully.")
            else:
                print("Specialist not found.")

        except Exception as e:
            print(f"Error occurred while removing patient: {e}")

    def find_patient_by_id(self, specialist_email, patient_id):
        try:
            # get the specialist document reference
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_data = specialist_ref[0].to_dict()
                patients = specialist_data.get('patients', [])

                # iterate through the patients to find the one with the specified ID
                for patient in patients:
                    if patient.get('id') == patient_id:
                        return patient
            return None

        except Exception as e:
            print(f"Error occurred while finding patient: {e}")
            return None

    def assign_test(self, specialist_email, patient_id, test_assigned, finished_current_test, due_date, due_hour, test_id, time_elapsed):
        try:
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_doc = specialist_ref[0].reference

                # get the current list of patients
                patients = specialist_ref[0].to_dict().get('patients', [])

                # find the patient with the provided ID
                for patient in patients:
                    if 'id' in patient and patient['id'] == patient_id:
                        # update the patient's test assignment and due date
                        patient['current_test_assigned'] = test_assigned
                        patient['finished_current_test'] = finished_current_test
                        patient['due_date'] = due_date
                        patient['due_hour'] = due_hour
                        patient['test_id'] = test_id
                        patient['time_elapsed'] = time_elapsed
                        break

                # update the 'patients' array field in the specialist's document with the updated patient data
                specialist_doc.update({'patients': patients})

                print("Test assigned successfully.")
            else:
                print("Specialist not found.")

        except Exception as e:
            print(f"Error occurred while assigning test: {e}")


    def generate_unique_patient_id(self, length=8):
        characters = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(characters) for _ in range(length))
        return unique_id


    def generate_unique_test_id(self, length=10):
        characters = string.ascii_letters + string.digits
        unique_id = ''.join(random.choice(characters) for _ in range(length))
        return unique_id

    def get_test_id(self, specialist_email, patient_id):
        try:
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_data = specialist_ref[0].to_dict()

                patients = specialist_data.get('patients', [])

                for patient in patients:
                    if patient.get('id') == patient_id:

                        return patient.get('test_id')
            return None

        except Exception as e:
            print(f"Error occurred while getting test ID: {e}")
            return None

    def get_answers_by_test_id(self, test_id):
        try:
            # query the answers collection for the given test ID
            query = self.answers_ref.where('test_id', '==', test_id).limit(1).get()

            # check if any documents were found
            for doc in query:
                return doc.to_dict().get('answers')

        except Exception as e:
            print(f"Error fetching answers: {e}")
            return None

    # databaseteki users dokumanın altındaki herşeyi iterate ettigi için efficient değil
    def update_patient(self, patient):
        try:
            patient_id = patient['id']

            # fetch all specialists
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                # check if the patient is in the list of patients for this specialist
                for p in patients:
                    if p.get('id') == patient_id:
                        specialist_doc = specialist_ref.reference

                        # update patient's data
                        updated_patients = [p if p.get('id') != patient_id else patient for p in patients]

                        # update the 'patients' array field in the specialist's document
                        specialist_doc.update({'patients': updated_patients})

                        print("Patient updated successfully.")
                        return

            print("Patient not found.")

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")

    def get_patient_name(self, patient_id):
        try:
            # fetch all specialists
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                # check if the patient is in the list of patients for this specialist
                for p in patients:
                    if p.get('id') == patient_id:
                        return p.get('name')

            print("Patient not found.")

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")

    def get_patient_age(self, patient_id):
        try:
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                for p in patients:
                    if p.get('id') == patient_id:
                        birthday_str = p.get('birthday')
                        if birthday_str:
                            birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
                            today = datetime.today()
                            age = today.year - birthday.year - (
                                        (today.month, today.day) < (birthday.month, birthday.day))
                            return age

            print("Patient not found.")
            return None

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")
            return None

    def get_patient_gender(self, patient_id):
        try:
            # fetch all specialists
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                # check if the patient is in the list of patients for this specialist
                for p in patients:
                    if p.get('id') == patient_id:
                        return p.get('gender')

            print("Patient not found.")

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")

    def get_patient_test_status(self, patient_id):
        try:
            # fetch all specialists
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                # check if the patient is in the list of patients for this specialist
                for p in patients:
                    if p.get('id') == patient_id:
                        return p.get('finished_current_test')

            print("Patient not found.")

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")

    def get_patient_answers(self, patient_id, answers_ref):
        try:
            # find the patient's test_id by iterating through specialists
            patient_test_id = None
            all_specialists = self.users_ref.stream()
            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])
                for patient in patients:
                    if patient.get('id') == patient_id:
                        patient_test_id = patient.get('test_id')
                        break

                if patient_test_id:
                    break

            if not patient_test_id:
                print("Patient's test_id not found.")
                return None

                # iterate through answers_ref to find matching test_id
            for answer_doc in answers_ref.stream():
                answer_data = answer_doc.to_dict()
                if answer_data.get('test_id') == patient_test_id:
                    return answer_data.get('answers', [])  # return the 'answers' array

            print("No matching answers found for the patient's test_id.")
            return None

        except Exception as e:
            print(f"Error occurred while retrieving patient answers: {e}")
            return None

    def get_patient_elapsedTime(self, test_id):
        try:
            # fetch all specialists
            all_specialists = self.users_ref.stream()

            for specialist_ref in all_specialists:
                specialist_data = specialist_ref.to_dict()
                patients = specialist_data.get('patients', [])

                # check if the patient is in the list of patients for this specialist
                for p in patients:
                    #print(p.get('test_id'), " " , test_id, " ", p.get('time_elapsed'))
                    if p.get('test_id') == test_id:
                        return p.get('time_elapsed')

            print("Patient not found.")

        except Exception as e:
            print(f"Error occurred while updating patient: {e}")

    def remove_test_link(self, specialist_email, patient_id):
        try:
            specialist_ref = self.users_ref.where('email', '==', specialist_email).limit(1).get()

            if specialist_ref:
                specialist_doc = specialist_ref[0].reference

                # get the current list of patients
                specialist_data = specialist_ref[0].to_dict()
                patients = specialist_data.get('patients', [])

                # iterate through patients to find the one with the provided ID
                for patient in patients:
                    if patient.get('id') == patient_id:
                        # remove test link from the patient's data
                        patient['current_test_assigned'] = ""
                        patient['finished_current_test'] = "Bitmedi"
                        patient['due_date'] = ""
                        patient['due_hour'] = ""
                        patient['test_id'] = ""
                        patient['time_elapsed'] = ""

                        # update the 'patients' array field in the specialist's document with the updated patient data
                        specialist_doc.update({'patients': patients})

                        print("Test link removed successfully.")
                        return

                print("Patient not found.")
            else:
                print("Specialist not found.")

        except Exception as e:
            print(f"Error occurred while removing test link: {e}")







import json

class TestsHandler:
    def __init__(self, db, users_ref):
        self.db = db
        self.users_ref = users_ref

    def get_fixed_questions(self):
        try:
            with open('fixed_questions.json', 'r', encoding='utf-8') as f:
                fixed_questions = json.load(f)
            return fixed_questions
        except Exception as e:
            print(f"Error occurred while reading fixed questions: {e}")
            return None


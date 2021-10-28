import json
from logging import Logger


class QuestionStore:

    def __init__(self, data_file) -> None:

        self.data_file = data_file
        self.posted_questions = None
        self.requested_questions = None

        q = self.__read_questions_json()
        self.posted_questions = q['posted_problem_ids']
        self.requested_questions = q['requested_problem_ids']

    def __read_questions_json(self) -> dict:
        try:
            with open(self.data_file) as f:
                return json.loads(f.read())
        except Exception as e:
            return {'posted_problem_ids': [], 'requested_problem_ids': []}

    def write_posted_questions(self, data_file=None):
        if data_file is None:
            data_file = self.data_file

        with open(self.data_file, mode='w') as f:
            json.dump(self.questions, f)

    def add_posted_question_id(self, question_id):
        self.questions['posted_problem_ids'].append(question_id)

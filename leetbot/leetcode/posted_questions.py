import json
import os


class PostedLeetCodeQuestions:

    def __init__(self, data_file) -> None:
        self.data_file = data_file
        self.questions = self.__read_posted_questions()

    def __read_posted_questions(self) -> dict:
        try:
            with open(self.data_file) as f:
                return json.loads(f.read())
        except:
            return {'posted_problem_ids': []}

    def write_posted_questions(self, data_file=None):
        if data_file is None:
            data_file = self.data_file

        with open(self.data_file, mode='w') as f:
            json.dump(self.questions, f)

    def add_posted_question_id(self, question_id):
        self.questions['posted_problem_ids'].append(question_id)

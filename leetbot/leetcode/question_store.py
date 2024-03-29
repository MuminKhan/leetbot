import json

class QuestionStore:

    def __init__(self, data_file: str) -> None:
        """Constructs the QuestionStore

        Args:
            data_file (str): Path to json datafile
        """
        self.data_file = data_file
        self._posted_questions_key = 'posted_problem_ids'
        self._requested_questions_key = 'requested_problem_ids'
        
        q = self.__read_questions_json(data_file=data_file)
        self.posted_questions: list    = q.get(self._posted_questions_key, [])   
        self.requested_questions: list = q.get(self._requested_questions_key, [])

    def __read_questions_json(self, data_file) -> dict:
        try:
            with open(data_file) as f:
                return json.loads(f.read())
        except Exception as e:
            return {self._posted_questions_key: [], self._requested_questions_key: []}

    def as_dict(self) -> dict:
        """Returns the QuestionStore as a dict

        Returns:
            dict: QuestionStore as {posted_problem_ids: [ids], requested_problem_ids: [ids]}
        """
        return {
            self._posted_questions_key:     self.posted_questions, 
            self._requested_questions_key:  self.requested_questions, 
        }

    def write_posted_questions(self, data_file=None):
        if data_file is None:
            data_file = self.data_file

        with open(self.data_file, mode='w') as f:
            json.dump(self.as_dict(), f)

    def add_posted_question_id(self, question_id):
        self.posted_questions.append(question_id)
        try:
            self.requested_questions.remove(question_id)
        except ValueError:
            pass
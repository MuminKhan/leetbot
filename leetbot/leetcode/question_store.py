import json

from boto3 import client


class QuestionStore:

    def __init__(self, data_file_path: str) -> None:
        """Constructs the QuestionStore

        Args:
            data_file (str): Path to json datafile
        """
        self.data_file_path = data_file_path
        self._posted_questions_key = "posted_problem_ids"
        self._requested_questions_key = "requested_problem_ids"

        q = self.__read_questions_json(data_file_path=data_file_path)
        self.posted_questions: list = q.get(self._posted_questions_key, [])
        self.requested_questions: list = q.get(self._requested_questions_key, [])

    def __is_s3_path(self, data_file_path: str) -> bool:
        return data_file_path.startswith("s3://")

    def __new_question_dict(self) -> dict:
        return {
            self._requested_questions_key: [],
            self._posted_questions_key: [],
        }

    def __read_questions_json(self, data_file_path: str) -> dict:
        if self.__is_s3_path(data_file_path):
            s3_prefix_len = len("s3://")
            bucket, key = data_file_path[s3_prefix_len:].split("/", 1)
            s3 = client("s3")

            # check to see if the file exists
            try:
                s3.head_object(Bucket=bucket, Key=key)
            except Exception:
                return self.__new_question_dict()

            obj = s3.get_object(Bucket=bucket, Key=key)
            return json.loads(obj["Body"].read().decode("utf-8"))

        try:
            with open(data_file_path) as f:
                return json.loads(f.read())
        except Exception:
            return self.__new_question_dict()

    def as_dict(self) -> dict:
        """Returns the QuestionStore as a dict

        Returns:
            dict: QuestionStore as {posted_problem_ids: [ids], requested_problem_ids: [ids]}
        """
        return {
            self._posted_questions_key: self.posted_questions,
            self._requested_questions_key: self.requested_questions,
        }

    def write_posted_questions(self, data_file_path=None):
        if data_file_path is None:
            data_file_path = self.data_file_path

        if self.__is_s3_path(data_file_path):
            s3_prefix_len = len("s3://")
            bucket, key = data_file_path[s3_prefix_len:].split("/", 1)
            s3 = client("s3")
            s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(self.as_dict()))
            return

        with open(self.data_file_path, mode="w") as f:
            json.dump(self.as_dict(), f)

    def add_posted_question_id(self, question_id):
        self.posted_questions.append(question_id)
        try:
            self.requested_questions.remove(question_id)
        except ValueError:
            pass

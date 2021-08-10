# /bin/python3

import json
import random
import urllib.request
from typing import DefaultDict

from leetcode.problem import LeetProblem


class LeetCodeQuestions:

    def __init__(self) -> None:
        self.LEETCODE_BASE_URL = "https://leetcode.com"
        self.LEETCODE_PROB_URL = f"{self.LEETCODE_BASE_URL}/problems"
        self.LEETCODE_QUES_URL = f"{self.LEETCODE_BASE_URL}/api/problems/all/"
        self.DESIRED_QUESTION_FIELDS = ['difficulty', 'frequency', 'frontend_question_id', 'paid_only',
                                        'question__article__has_video_solution', 'question__article__live', 'question__article__slug',
                                        'question__hide', 'question__title', 'question__title_slug',
                                        'question_id', 'status', 'total_acs', 'total_submitted']
        self.DIFFICULTY_MAPPING = {1: 'easy', 2: 'medium', 3: 'hard'}

        self.response = self.__get_leetcode_data(self.LEETCODE_QUES_URL)
        self.all_questions = self.__clean_questions(self.response)
        self.questions_by_id = self.__organize_questions_by_id(self.all_questions)
        self.questions_by_difficulty = self.__organize_questions_by_difficulty(self.all_questions)

    def __clean_questions(self, questions):
        all_questions = []
        for question in questions["stat_status_pairs"]:
            question.update(question["stat"])
            question.pop('stat')
            question["difficulty"] = self.DIFFICULTY_MAPPING[question["difficulty"]["level"]]
            all_questions.append(question)

        return all_questions

    def __organize_questions_by_difficulty(self, question_dict: dict) -> dict:
        questions_by_difficulty = DefaultDict(list)

        for q in question_dict:
            problem = LeetProblem(question_json=q)
            questions_by_difficulty[q["difficulty"]].append(problem)

        return questions_by_difficulty

    def __organize_questions_by_id(self, question_dict: dict) -> dict:
        questions_by_id = {}

        for q in question_dict:
            problem = LeetProblem(question_json=q)
            questions_by_id[q['question_id']] = problem

        return questions_by_id

    def __get_leetcode_data(self, url=None) -> dict:

        if url is None:
            url = self.LEETCODE_QUES_URL

        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        response = json.load(urllib.request.urlopen(request))
        return response

    def get_random_problem_id(self, ids_to_exclude=set(), filters=None):
        """
        Returns the id of a randomly selected question
        """
        ids_to_exclude = set(ids_to_exclude)
        possible_questions = set(self.questions_by_id.keys()) - ids_to_exclude
        return random.sample(possible_questions, 1)[0]

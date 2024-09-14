# /bin/python3

import json
import random
import urllib.request
from enum import Enum
from typing import DefaultDict

from leetcode.problem import LeetProblem
from leetcode.question_store import QuestionStore


class QuestionDifficulty(Enum):
    easy = 1
    medium = 2
    hard = 3


class LeetCodeQuestions:
    LEETCODE_BASE_URL = "https://leetcode.com"
    LEETCODE_PROB_URL = f"{LEETCODE_BASE_URL}/problems"
    LEETCODE_ALL_PROBLEMS_URL = f"{LEETCODE_BASE_URL}/api/problems/all"
    DESIRED_QUESTION_FIELDS = [
        "difficulty",
        "frequency",
        "frontend_question_id",
        "paid_only",
        "question__article__has_video_solution",
        "question__article__live",
        "question__article__slug",
        "question__hide",
        "question__title",
        "question__title_slug",
        "question_id",
        "status",
        "total_acs",
        "total_submitted",
    ]

    def __init__(self) -> None:

        self.response = self.__get_leetcode_data(LeetCodeQuestions.LEETCODE_ALL_PROBLEMS_URL)
        self.all_questions = self.__clean_questions(self.response)
        self.questions_by_id = self.__organize_questions_by_id(self.all_questions)
        self.questions_by_difficulty = self.__organize_questions_by_difficulty(self.all_questions)

    def __clean_questions(self, questions: dict):
        all_questions = []

        for question in questions["stat_status_pairs"]:
            question.update(question["stat"])
            question.pop("stat")
            question["difficulty"] = QuestionDifficulty(question["difficulty"]["level"])
            question["url"] = f'{LeetCodeQuestions.LEETCODE_PROB_URL}/{question["question__title_slug"]}'
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
            questions_by_id[q["question_id"]] = problem

        return questions_by_id

    def __get_leetcode_data(self, url=None) -> dict:

        if url is None:
            url = LeetCodeQuestions.LEETCODE_ALL_PROBLEMS_URL

        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
            },
        )
        response = json.load(urllib.request.urlopen(request))
        return response

    def get_problem_id(self, question_store):
        """
        Returns the id of a selected question
        """
        ids_to_exclude = set(question_store.posted_questions)
        possible_questions = [id for id in question_store.requested_questions if id not in ids_to_exclude]

        if len(possible_questions) == 0:
            possible_questions = list(set(self.questions_by_id.keys()) - ids_to_exclude)
            problem_id = random.choice(possible_questions)
        else:
            problem_id = possible_questions[0]

        return problem_id

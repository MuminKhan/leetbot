# /bin/python3

import json
from typing import DefaultDict
import urllib.request


class LeetCode:

    def __init__(self) -> None:
        self.LEETCODE_BASE_URL = "https://leetcode.com"
        self.LEETCODE_PROB_URL = f"{self.LEETCODE_BASE_URL}/problems"
        self.LEETCODE_QUES_URL = f"{self.LEETCODE_BASE_URL}/api/problems/all/"
        self.DESIRED_QUESTION_FIELDS = ['difficulty', 'frequency', 'frontend_question_id', 'paid_only',
                                   'question__article__has_video_solution', 'question__article__live', 'question__article__slug',
                                   'question__hide', 'question__title', 'question__title_slug',
                                   'question_id', 'status', 'total_acs', 'total_submitted']
        self.DIFFICULTY_MAPPING = {1: 'easy', 2: 'medium', 3: 'hard'}

        response = self.get_leetcode_data(self.LEETCODE_QUES_URL)
        json_response = json.load(response)

        self.questions_by_id = self.__organize_questions_by_id(json_response)
        self.questions_by_difficulty = self.__organize_questions_by_difficulty(json_response)

    def get_leetcode_data(self, url) -> dict:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
        response = urllib.request.urlopen(request)
        return response

    def __organize_questions_by_id(self, question_dict: dict) -> dict:
        questions_by_id = {}

        all_questions = question_dict["stat_status_pairs"]
        for q in all_questions:
            q.update(q["stat"])
            q.pop('stat')
            q["difficulty"] = self.DIFFICULTY_MAPPING[q["difficulty"]["level"]]
            questions_by_id[q['question_id']] = q

        return questions_by_id

    def __organize_questions_by_difficulty(self, question_dict: dict) -> dict:
        questions_by_difficulty = DefaultDict(list)

        all_questions = question_dict["stat_status_pairs"]
        for q in all_questions:
            questions_by_difficulty[q["difficulty"]].append(q)

        return questions_by_difficulty

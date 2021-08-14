
import argparse
import logging

import slack_client.client
from leetcode.posted_questions import PostedLeetCodeQuestions
from leetcode.questions import LeetCodeQuestions
from leetcode.problem import LeetProblem


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--channel',    '-c', required=True,  dest='channel',    action='store', help='Channel to post to. Bot must be a member to post.')
    parser.add_argument('--data_file',  '-D', required=False, dest='data_file',  action='store', help='Where to read/write posted questions. Default="./leetbot.json"', default='leetbot.json')
    parser.add_argument('--difficulty', '-d', required=False, dest='difficulty', action='store', help='List of any combination of [easy, medium, hard]', type=str, default='easy,medium,hard')

    args = parser.parse_args()
    args.difficulty = args.difficulty.lower()

    print('Args:')
    [print(f'\t{k}: {v}') for k, v in args.__dict__.items()]

    return args


def get_question(posted_questions: list) -> LeetProblem:

    lc = LeetCodeQuestions()
    problem = id = None
    while id is None:
        id = lc.get_random_problem_id(set())
        problem = lc.questions_by_id[id]
        if problem.difficulty not in args.difficulty:
            id = None

    return problem


def build_message(question: LeetProblem):
    body = f"*Today's LeetCode Question incoming @channel!*"
    body += f'\tTitle:      {question.question_title.title()}\n'
    body += f'\tProblem ID: {question.question_id}\n'
    body += f'\tDifficulty: {question.difficulty.title()}\n'
    body += f'\tURL: {question.url}\n'
    message = {
        "channel": args.channel,
        "unfurl_links": True,
        "unfurl_media": False,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": body,
                }
            }
        ]
    }
    return message


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
if __name__ == "__main__":

    args = parse_args()
    posted_questions = PostedLeetCodeQuestions(args.data_file)
    problem = get_question(posted_questions)
    message = build_message(problem)

    if message is None:
        print('Nothing to post...')
        exit()

    response = slack_client.client.post_to_slack(message)
    if response is not None:
        posted_questions.add_posted_question_id(problem.question_id)
        posted_questions.write_posted_questions()

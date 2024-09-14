import logging

import slack_client.client
from leetcode.problem import LeetProblem
from leetcode.question_store import QuestionStore
from leetcode.questions import LeetCodeQuestions
from utils.cli_args import parse_args
from utils.config import config

logging.getLogger().setLevel(logging.INFO)


def get_question(questions: dict) -> LeetProblem:

    lc = LeetCodeQuestions()
    problem = problem_id = None
    while problem_id is None:
        problem_id = lc.get_problem_id(questions)
        problem = lc.questions_by_id[problem_id]
        if problem.difficulty.name not in config.difficulty or problem.paid_only:
            problem_id = None

    return problem


def build_message(question: LeetProblem):
    text = f"New LeetCode Question posted in #{config.channel}!"
    body = f"*Today's LeetCode Question incoming{' @channel' if config.alert else ''}!*\n"
    body += f"\tName: {question.question_title}\n"
    body += f"\tID: {question.question_id}\n"
    body += f"\tLevel: {question.difficulty.name}\n"
    body += f"\tURL: {question.url}\n"
    message = {
        "channel": config.channel,
        "unfurl_links": True,
        "unfurl_media": False,
        "text": text,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": body,
                },
            }
        ],
    }
    return message


def cli_handler():
    logging.info("Starting Leetbot from CLI.")
    logging.info("Parsing CLI args.")
    args = parse_args()
    config.channel = args.channel if args.channel else config.channel
    config.difficulty = args.difficulty if args.difficulty else config.difficulty
    config.alert = args.alert if args.alert else config.alert
    config.data_file = args.data_file if args.data_file else config.data_file

    return handler(None, None)


def handler(event, context):
    logging.info("Starting Leetbot from Lambda.")
    logging.info(event)
    logging.info(context)
    logging.info(str(config))

    logging.info("Reading questions store.")
    questions_store = QuestionStore(config.data_file)

    logging.info("Getting question.")
    problem = get_question(questions_store)

    logging.info(f"Posting question: {problem.question_id}")
    message = build_message(problem)

    logging.info(f"Posting to Slack: {message}")
    response = slack_client.client.post_to_slack(message)
    if response is not None:
        questions_store.add_posted_question_id(problem.question_id)
        questions_store.write_posted_questions()

    logging.info("Leetbot finished.")
    return response


if __name__ == "__main__":
    cli_handler()

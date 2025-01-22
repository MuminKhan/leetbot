import logging

import slack_client.client
from leetcode.problem import LeetProblem
from leetcode.question_store import QuestionStore
from leetcode.questions import LeetCodeQuestions
from utils.cli_args import parse_args
from utils.config import config

logging.getLogger().setLevel(logging.INFO)


def get_questions(questions: dict) -> LeetProblem:
    lc = LeetCodeQuestions()
    problems = []

    while len(problems) < config.quantity:
        problem_id = lc.get_problem_id(questions)
        problem = lc.questions_by_id[problem_id]
        if problem.difficulty.name not in config.difficulty or problem.paid_only:
            continue
        problems.append(problem)

    return problems


def build_message(questions: list[LeetProblem]):
    text = f"New LeetCode Question posted in #{config.channel}!"
    body = f"*Today's LeetCode Questions incoming{' @channel' if config.alert else ''}!*\n"

    for question in questions:
        body += f"Name: {question.question_title}\n"
        body += f"\tID: {question.question_id}\n"
        body += f"\tLevel: {question.difficulty.name}\n"
        body += f"\tURL: {question.url}\n"

    if config.meeting_time and config.meeting_link:
        body += f"Please join us today at {config.meeting_time} at {config.meeting_link}\n."

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

    logging.info("Getting questions.")
    problems = get_questions(questions_store)

    logging.info(f"Posting questions: {", ".join([str(p.question_id) for p in problems])}")
    message = build_message(problems)

    logging.info(f"Posting to Slack: {message}")
    response = slack_client.client.post_to_slack(message)
    if response["status"] == "success":
        for problem in problems:
            questions_store.add_posted_question_id(problem.question_id)
        questions_store.write_posted_questions()

    logging.info(f"Response: {response}")
    logging.info("Leetbot finished.")
    return response


if __name__ == "__main__":
    cli_handler()

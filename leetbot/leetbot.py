import slack_client.client
import utils.cli_args

from leetcode.problem import LeetProblem
from leetcode.question_store import QuestionStore
from leetcode.questions import LeetCodeQuestions
from utils.logger import logger


def get_question(questions: dict) -> LeetProblem:

    lc = LeetCodeQuestions()
    problem = problem_id = None
    while problem_id is None:
        problem_id = lc.get_problem_id(questions)
        problem = lc.questions_by_id[problem_id]
        if problem.difficulty.name not in args.difficulty or problem.paid_only:
            problem_id = None

    return problem


def build_message(question: LeetProblem):
    text = f"New LeetCode Question posted in #{args.channel}!"
    body = f"*Today's LeetCode Question incoming{' @channel' if args.alert else ''}!*\n"
    body += f"\tName: {question.question_title}\n"
    body += f"\tID: {question.question_id}\n"
    body += f"\tLevel: {question.difficulty.name}\n"
    body += f"\tURL: {question.url}\n"
    message = {
        "channel": args.channel,
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
    logger.debug("Starting Leetbot from CLI.")
    logger.debug("Parsing CLI args.")
    args = cli_handler.parse_args()

    return handler()


def handler(event, context):

    logger.log(event)
    logger.log(context)
    return context

    questions_store = QuestionStore(args.data_file)
    problem = get_question(questions_store)
    message = build_message(problem)

    if message is None:
        print("Nothing to post...")
        exit()

    response = slack_client.client.post_to_slack(message)
    if response is not None:
        questions_store.add_posted_question_id(problem.question_id)
        questions_store.write_posted_questions()

    return response

import argparse
import logging

import slack_client.client
from leetcode.question_store import QuestionStore
from leetcode.questions import LeetCodeQuestions
from leetcode.problem import LeetProblem


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--channel",
        "-c",
        required=True,
        dest="channel",
        action="store",
        help="Channel to post to. Bot must be a member to post.",
    )
    parser.add_argument(
        "--alert", required=False, dest="alert", action="store_true", help="Whether or not to send an @here alert."
    )
    parser.add_argument(
        "--data_file",
        "-D",
        required=False,
        dest="data_file",
        action="store",
        help='Where to read/write posted questions. Default="./leetbot.json"',
        default="leetbot.json",
    )
    parser.add_argument(
        "--difficulty",
        "-d",
        required=False,
        dest="difficulty",
        action="store",
        help="List of any combination of [easy, medium, hard]",
        type=str,
        default="easy,medium,hard",
    )

    args = parser.parse_args()
    args.difficulty = args.difficulty.lower()

    print("Args:")
    [print(f"\t{k}: {v}") for k, v in args.__dict__.items()]

    return args


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


def main():
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


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    args = parse_args()
    main()


import argparse
import logging

import data
import slack_utils
from leetcode import LeetCode
from studybot import StudyBot


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--channel',   '-c', required=True,  dest='channel',       action='store', help='Channel to post to. Bot must be a member to post.')
    parser.add_argument('--manifest',  '-m', required=True,  dest='manifest_file', action='store', help='Location of manifest file. Must be a .csv or .json.')
    parser.add_argument('--template',  '-t', required=True,  dest='template_file', action='store', help='Template file location')
    parser.add_argument('--data_file', '-d', required=False, dest='data_file',     action='store', help='Where to read/write posted questions. Default="./algobot.json"', default='algobot.json')

    args = parser.parse_args()

    print('Args:')
    [print(f'\t{k}: {v}') for k, v in args.__dict__.items()]

    return args


if __name__ == "__main__":  # entrypoint

    args = parse_args()

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    posted_questions = data.read_posted_questions(args.data_file)

    lc = LeetCode()
    all_questions = lc.questions_by_id


    bot = StudyBot(args.channel, args.manifest_file, args.template_file)
    message = bot.get_message_payload()

    response = None
    if message is not None:
        response = slack_utils.post_to_slack(message)
    else:
        print('Nothing to post...')

    print(f"\n\n\nRESPONSE: \n{str(response)}") if response is not None else print('')

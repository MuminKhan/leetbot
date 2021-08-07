
import argparse
import logging

import slack_client.client
from leetcode.posted_questions import PostedLeetCodeQuestions
from leetcode.questions import LeetCodeQuestions


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--channel',   '-c', required=True,  dest='channel',       action='store', help='Channel to post to. Bot must be a member to post.')
    #parser.add_argument('--manifest',  '-m', required=True,  dest='manifest_file', action='store', help='Location of manifest file. Must be a .csv or .json.')
    #parser.add_argument('--template',  '-t', required=True,  dest='template_file', action='store', help='Template file location')
    parser.add_argument('--data_file', '-D', required=False, dest='data_file',  action='store', help='Where to read/write posted questions. Default="./leetbot.json"', default='leetbot.json')
    parser.add_argument('--difficulty','-d', required=False, dest='difficulty', action='store', help='List of any combination of [easy, medium, hard]', type=str, default=['easy', 'medium', 'hard'])

    args = parser.parse_args()
    args.difficulty = args.difficulty.lower() 

    print('Args:')
    [print(f'\t{k}: {v}') for k, v in args.__dict__.items()]

    return args


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
if __name__ == "__main__":

    args = parse_args()

    posted_questions = PostedLeetCodeQuestions(args.data_file)
    
    lc = LeetCodeQuestions()
    problem = id = None 
    while id is None:
        id = lc.get_random_problem_id(set())
        problem = lc.questions_by_id[id]
        if problem.difficulty not in args.difficulty:
            id = None 
        
    [print(k,v) for k,v in problem.__dict__.items() if 'json' not in k]
    
    message = {
        "channel": args.channel,
        "unfurl_links": False,
        "unfurl_media": False,
        "blocks": []
    }

    response = None
    if message is not None:
        response = slack_client.client.post_to_slack(message)
    else:
        print('Nothing to post...')

    print(f"\n\n\nRESPONSE: \n{str(response)}") if response is not None else print('')

    posted_questions.add_posted_question_id(id)
    posted_questions.write_posted_questions()

import json
import os

def read_posted_questions(data_file) -> dict:

    if not os.path.exists(data_file):
        return {'posted_problem_ids' : []}

    with open(data_file) as f:
        probs = json.loads(f.read())

    return probs


def write_posted_questions(data_file, posted_probs):
    with open(data_file, mode='w') as f:
        json.dump(posted_probs, data_file)


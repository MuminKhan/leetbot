import sys

sys.path.append('src')

import app
from studybot import StudyBot


def test_studybot_post():
    app.post_to_slack(app.slack_web_client, app.get_message())


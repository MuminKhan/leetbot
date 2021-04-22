import json
from datetime import date

import message_utils


class StudyBot:

    def __init__(self, channel, manifest_file, template_file):
        self.today = date.today().strftime("%Y-%m-%d")
        self.channel = channel
        self.manifest_file = manifest_file
        self.template_file = template_file

    def _get_entries_from_manifest(self) -> dict:
        with open(self.manifest_file, 'r') as f:
            manifest = json.loads(f.read())
        return manifest[self.today]

    def _build_messages(self, date_entries):
        template = message_utils.get_message_template(self.template_file)
        messages = []
        
        for entry in date_entries:
            message = message_utils.parse_template(template, entry)
            block = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (message),
                },
            }
            messages.append(block)
        return messages

    def get_message_payload(self) -> dict:
        date_entries = self._get_entries_from_manifest()
        messages = self._build_messages(date_entries)
        return {
            "channel": self.channel,
            "blocks": [
                *messages,
            ],
        }

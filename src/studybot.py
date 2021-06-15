import json
from datetime import date

import message_utils


class StudyBot:

    def __init__(self, channel, manifest_file, template_file):
        self.today = date.today().strftime("%Y-%m-%d")
        self.channel = channel
        self.manifest_file = manifest_file
        self.template_file = template_file

    def _get_entries_from_json_manifest(self) -> dict:
        with open(self.manifest_file, 'r') as f:
            manifest = json.loads(f.read())

        return manifest.get(self.today, [])

    def _get_entries_from_csv_manifest(self) -> dict:
        manifest = {}
        header = None
        with open(self.manifest_file, 'r') as f:
            while True:
                line = [s.strip() for s in f.readline().split(',')]
                if header is None:
                    header = line
                    continue

                if line == ['']:
                    break

                if manifest.get(line[0]) is None:
                    manifest[line[0]] = []
                
                if len(line) == len(header):
                    manifest[line[0]].append({k:v for k,v in zip(header[1:], line[1:])})
                else:
                    print(f"Malformed line: {line}")

        return manifest.get(self.today, [])


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

        if '.csv' in self.manifest_file.lower():
            date_entries = self._get_entries_from_csv_manifest()
        elif '.json' in self.manifest_file.lower():
            date_entries = self._get_entries_from_json_manifest()
        else:
            raise Exception(f'{self.manifest_file} does not appear to be a CSV or JSON.')
        
        messages = self._build_messages(date_entries)
        if len(messages) == 0:
            return None

        return {
            "channel": self.channel,
            "unfurl_links": False,
            "unfurl_media": False,
            "blocks": [
                *messages,
            ],
        }

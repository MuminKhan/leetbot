import json

from schemas.cs61b_schema import CS61B
from datetime import date


class AlgoBot:

    def __init__(self, channel, manifest_file):
        self.today = date.today().strftime("%Y-%m-%d")
        self.channel = channel
        self.manifest_file = manifest_file

    def _get_entries_from_manifest(self) -> dict:
        with open(self.manifest_file, 'r') as f:
            manifest = json.loads(f.read())

        return manifest[self.today]

    def _build_messages(self, date_entries):

        messages = []

        for entry in date_entries:

            message = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"CS61B for {self.today}: " + f"{entry[CS61B.lecture_title]}\n" +
                        "\tReading: "               + f"{entry[CS61B.reading]}\n" +
                        "\tVideos: "                + f"{entry[CS61B.lecture_video]}\n" + 
                        "\tGuide: "                 + f"{entry[CS61B.lecture_guide]}\n" +
                        "\tDiscussion: "            + f"{entry[CS61B.discussion_worksheet]}\n" + 
                        "\tDiscussion Solution: "   + f"{entry[CS61B.discussion_solution]}" 
                    ),
                },
            }
            messages.append(message)

        print(len(messages))
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

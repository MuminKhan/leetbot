from os import environ


class Config(object):

    LEETBOT_CHANNEL: str = "LEETBOT_CHANNEL"
    LEETBOT_JSON_PATH: str = "LEETBOT_JSON_PATH"
    LEETBOT_QUESTION_DIFFICULTY: str = "LEETBOT_QUESTION_DIFFICULTY"
    LEETBOT_QUESTION_QUANTITY: str = "LEETBOT_QUESTION_QUANTITY"
    LEETBOT_SEND_CHANNEL_ALERT: str = "LEETBOT_SEND_CHANNEL_ALERT"
    LEETBOT_SLACK_TOKEN: str = "LEETBOT_SLACK_TOKEN"
    DIFFICULTY_OPTIONS: set[str] = {"easy", "medium", "hard"}

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.alert: bool = environ.get(Config.LEETBOT_SEND_CHANNEL_ALERT, False)
        self.channel: str = environ.get(Config.LEETBOT_CHANNEL, None)
        self.data_file: str = environ.get(Config.LEETBOT_JSON_PATH, "leetbot.json")
        self.difficulty: set[str] = environ.get(Config.LEETBOT_QUESTION_DIFFICULTY, Config.DIFFICULTY_OPTIONS)
        self.quantity: int = int(environ.get(Config.LEETBOT_QUESTION_QUANTITY, 1))
        self.slack_token: str = environ.get(Config.LEETBOT_SLACK_TOKEN, None)

        if not isinstance(self.alert, bool):
            self.alert = self.alert.lower() == "true"
        if not isinstance(self.difficulty, set):
            difficulty = set()
            for diff in self.difficulty.split(","):
                diff = diff.strip().lower()
                if diff in Config.DIFFICULTY_OPTIONS:
                    difficulty.add(diff)
            self.difficulty = difficulty

    def __str__(self) -> str:
        return f"Config:\n" + "\n".join(
            [f"\t{k}: {v}" for k, v in self.__dict__.items() if k not in {"instance", "slack_token"}]
        )


config = Config()


class LeetProblem:

    def __init__(self) -> None:
        self.question_id: int
        self.difficulty: str
        self.frequency: str
        self.frontend_question_id: str
        self.paid_only: bool
        self.question_article_has_video_solution: bool
        self.question_article_live: str
        self.question_article_slug: str
        self.question_hide:bool
        self.question_title: str
        self.question_title_slug: str
        self.status: str
        self.total_acs: int
        self.total_submitted: int 
        self.tags: str
        self.json: dict

    def __init__(self, question_json: dict) -> None:
        self.json = question_json
        for k,v in question_json.items():
            key = k.replace('__', '_')
            self.__dict__[key] = v
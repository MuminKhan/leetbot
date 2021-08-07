
class LeetProblem:

    def __init__(self) -> None:
        self.question_id
        self.difficulty
        self.frequency
        self.frontend_question_id
        self.paid_only
        self.question_article_has_video_solution
        self.question_article_live
        self.question_article_slug
        self.question_hide
        self.question_title
        self.question_title_slug
        self.status
        self.total_acs
        self.total_submitted 
        self.tags
        self.json

    def __init__(self, question_json) -> None:
        self.json = question_json
        for k,v in question_json.items():
            key = k.replace('__', '_')
            self.__dict__[key] = v
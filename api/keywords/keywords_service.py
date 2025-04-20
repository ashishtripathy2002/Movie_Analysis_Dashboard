class KeywordsService:
    def __init__(self, keywords_repository):
        self.keywords_repository = keywords_repository

    def get_all_keywords(self):
        return self.keywords_repository.get_all_keywords()
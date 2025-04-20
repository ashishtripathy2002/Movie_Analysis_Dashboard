from sqlalchemy import text


class KeywordsRepository:
    def __init__(self, db):
        self.db = db

    def get_all_keywords(self):
        query = text(f"""
                  SELECT keyword_id, keyword_name FROM keywords""")
        result = self.db.execute_dql_commands(query)
        data = result.fetchall() if result else []
        return [{"keyword_id": row.keyword_id, "keyword_name": row.keyword_name} for row in data]
from loguru import logger
from db_client import PostgresClient
from llm_client import OllamaClient

class IssueManager:
    def __init__(self, db: PostgresClient, llm: OllamaClient):
        self.db = db
        self.llm = llm

    def search_similar_issues(self, input, limit=5, vector_size=1024):
        input_embed = self.llm.embed(input)
        try:
            results = self.db.select(table="issues",
                                     columns="id, brand, model, issue, fix, issue_embedding <-> %s::vector(%s) AS distance",
                                     order_clause="distance",
                                     limit_clause=limit,
                                     params=(input_embed, vector_size))
            return results
        except Exception as e:
            logger.error(f"Error executing SELECT: {e}")
            return None
        
    def update_issue_embed(self, id, input):
        input_embed = self.llm.embed(input)
        try:
            set_clause = "issue_embedding = %s"
            where_clause = "id = %s"
            params = (input_embed, id)
            self.db.update('issues', set_clause, where_clause, params)            
        except Exception as e:
            logger.error(f"Error executing UPDATE: {e}")
            return None
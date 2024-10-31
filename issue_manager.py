from loguru import logger
import time
from db_client import PostgresClient
from llm_client import OllamaClient
import json

class IssueManager:
    def __init__(self, db: PostgresClient, llm: OllamaClient):
        self.db = db
        self.llm = llm

    def search_similar_issues(self, input, limit=5, vector_size=1024):
        input_embed = self.llm.embed(input)

        start_time = time.time()

        try:
            results = self.db.select(table="issues",
                                     columns="id, brand, model, issue, fix, issue_embedding <-> %s::vector(%s) AS distance",
                                     order_clause="distance",
                                     limit_clause=limit,
                                     params=(input_embed, vector_size))
            elapsed_time = time.time() - start_time
            logger.info(f"Search completed in {elapsed_time} seconds")
            json_result = self.__convert_results_to_json(results)
            logger.debug(f"Results: {json.dumps(json_result, indent=4)}")
            return json_result
        except Exception as e:
            logger.error(f"Error executing SELECT: {e}")
            return None
        
    def update_issue_embed(self, id, input):
        input_embed = self.llm.embed(input)
        try:
            set_clause = "issue_embedding = %s"
            where_clause = "id = %s"
            params = (input_embed, id)
            self.db.update(table='issues', set_clause=set_clause, where_clause=where_clause, params=params)            
        except Exception as e:
            logger.error(f"Error executing UPDATE: {e}")
            return None
    
    def __convert_results_to_json(self, results):
        json_results = []
        for row in results:
            json_results.append({
                "id": row[0],
                "brand": row[1],
                "model": row[2],
                "issue": row[3],
                "fix": row[4],
                "distance": row[5]
            })
        return json_results
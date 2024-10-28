from loguru import logger
import os
from dotenv import load_dotenv
import json
from db_client import PostgresClient
from llm_client import OllamaClient
from issue_manager import IssueManager

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

ollama_host = os.getenv("OLLAMA_HOST")
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_embed_model = os.getenv("OLLAMA_EMBED_MODEL")
vector_size = int(os.getenv("VECTOR_SIZE"))

db = PostgresClient(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
ollama_client = OllamaClient(host=ollama_host, model=ollama_model, embed_model=ollama_embed_model)
issue_manager = IssueManager(db, ollama_client)

prompt = """
    Generate a realistic mobile phone issue record. Include:
    - Brand
    - Model
    - Date
    - Issue
    - Fix
    The output must be a JSON containing above fields without any additional comments.
    There must be 25 records.
    Issue and Fix should be detailed, more or less 50 words for each.
    Records must be varied in terms of brand, model, and type of issues.
    The JSON format must be:
    {
        "record": [
            {
            "brand": "Apple",
            "model": "IPhone 13",
            "date": "2024-01-15",
            "issue": "Screen cracked after drop",
            "fix": "Replaced screen"
            },
            {
            "brand": "Samsung",
            "model": "Galaxy 22",
            "date": "2023-11-20",
            "issue": "Overheating during prolonged use",
            "fix": "Cleaned dust from vents and replaced CPU fan"
            }
        ]
    }
    """

for i in range(10):
    data = ollama_client.generate(prompt, format="json")
    jdata = json.loads(data)

    #print(type(jdata))
    #print(jdata)  

    for d in jdata["record"]:
        try:
            db.insert(
                table='issues',
                columns=['issue_date', 'brand', 'model', 'issue', 'fix'],
                values=[
                    d["date"],
                    d["brand"],
                    d["model"],
                    d["issue"],
                    d["fix"]
                ]
            )
        except Exception as e:
            logger.error("Error while fetching data: {}", e)
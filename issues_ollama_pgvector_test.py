import os
from dotenv import load_dotenv
import psycopg2
from db_client import Postgres
from ollama import Client

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

ollama_host = os.getenv("OLLAMA_HOST")
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_embed_model = os.getenv("OLLAMA_EMBED_MODEL")

db = Postgres(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)

ollama_client = Client(host=ollama_host)

# Get embeddings from Ollama
def get_embedding(text):
    response = ollama_client.embed(model=ollama_embed_model, input=text)
    return ",".join(map(str, response['embeddings']))

def update_issue(id, issue):
    embedding = get_embedding(issue)

    set_clause = "issue_embedding = %s"
    where_clause = "id = %s"
    params = (embedding, id)
    db.update('issues', set_clause, where_clause, params)

# Generate embeddings for issues
issues = db.select('issues', columns='id, issue')

for i, (id, issue) in enumerate(issues, 1):
    print(f"{i}: ID = {id}, Issue = {issue}")
    update_issue(id, issue)

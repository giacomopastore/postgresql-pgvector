import os
from dotenv import load_dotenv
from db_client import PostgresClient
from llm_client import OllamaClient

load_dotenv()

db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

ollama_host = os.getenv("OLLAMA_HOST")
ollama_model = os.getenv("OLLAMA_MODEL")
ollama_embed_model = os.getenv("OLLAMA_EMBED_MODEL")

db = PostgresClient(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)

ollama_client = OllamaClient(host=ollama_host)

# Update issue with embedding
def update_issue(id, issue):
    embedding = ollama_client.get_embedding(model=ollama_embed_model, input=issue)

    set_clause = "issue_embedding = %s"
    where_clause = "id = %s"
    params = (embedding, id)
    db.update('issues', set_clause, where_clause, params)

# Generate embeddings for issues
issues = db.select('issues', columns='id, issue', where_clause='issue_embedding IS NULL')

for i, (id, issue) in enumerate(issues, 1):
    print(f"{i}: ID = {id}, Issue = {issue}")
    update_issue(id, issue)

# Serch for similar issues
search_query = "cannot connect to bluetooth devices"
query_embedding = embedding = ollama_client.get_embedding(model=ollama_embed_model, input=search_query)
results = db.search_similar_issues(query_embedding)

print(f"Search results for: '{search_query}'")
for i, (id, issue, distance) in enumerate(results, 1):
    print(f"{i}. {id} - {issue} (Distance: {distance:.4f})")

db.close()
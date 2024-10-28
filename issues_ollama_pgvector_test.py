from loguru import logger
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
vector_size = int(os.getenv("VECTOR_SIZE"))

db = PostgresClient(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)

ollama_client = OllamaClient(host=ollama_host)

# Update issue with embedding
def update_issue(id, issue):
    embedding = ollama_client.embed(model=ollama_embed_model, input=issue)

    set_clause = "issue_embedding = %s"
    where_clause = "id = %s"
    params = (embedding, id)
    db.update('issues', set_clause, where_clause, params)

# Generate embeddings for issues
issues = db.select('issues', columns='id, brand, model, issue', where_clause='issue_embedding IS NOT NULL')

for i, (id, brand, model, issue) in enumerate(issues, 1):
    print(f"{i}: ID = {id}, Issue = {issue}")
    update_issue(id, f"{brand} - {model} - {issue}")

# Serch for similar issues
#search_query = "I have a wifi problem with my iphone"
search_query = "I'm not able to hear the call from my iphone"
query_embedding = embedding = ollama_client.embed(model=ollama_embed_model, input=search_query)
results = db.search_similar_issues(query_embedding, vector_size=vector_size)

print(f"Search results for: '{search_query}'")
for i, (id, brand, model, issue, fix, distance) in enumerate(results, 1):
    print(f"{i}. {id} - {brand} - {model} - {issue} (Distance: {distance:.4f})")

# Propose a solution
# Version 1
prompt = ("You are an assistant who can provide help and advice on how to solve any problems and defects of smartphones."
        "You need to start the chat by summarizing the problem exposed by the user and explain some solutions."
        "You only need to elaborate the following possible solutions and not to give alternative solutions based on your knowledge base."
        "If there are no possible solutions you just need to say that unfortunately you can't give help."
        f"Here the question from the user '{search_query}', here possible solutions:\n"
        f"{'\n'.join(f'- ({brand} {model}): {fix}' for (id, brand, model, issue, fix, distance) in results)}\n")

# Version 2
data = '\n'.join(f'- ({brand} {model}): {fix}' for (id, brand, model, issue, fix, distance) in results)
prompt = f"Using this data: {data}. Respond to this prompt: {search_query}"

response = ollama_client.generate(model=ollama_model, prompt=prompt)
print(response)

db.close()
from loguru import logger
import os
from dotenv import load_dotenv
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

# Generate embeddings for issues
issues = db.select('issues', columns='id, brand, model, issue', where_clause='issue_embedding IS NULL')

for (id, brand, model, issue) in issues:
    issue_manager.update_issue_embed(id, f"Brand: {brand}, Model: {model}, Issue: {issue}")

# Serch for similar issues
#search_query = "I have a wifi problem with my iphone 13"
#search_query = "I'm not able to hear the call from my iphone"
#search_query = "Face authentication no longer works on my iPhone 13"
#search_query = "On my oneplus bluetooth seems not working fine"
#search_query = "How can I resolve problems on detecting WiFi network with my Poco F3?"
search_query = "I have a Galaxy A52 and sometimes it reboots."
results = issue_manager.search_similar_issues(input=search_query)

print(f"Search results for: '{search_query}'")
for i, (id, brand, model, issue, fix, distance) in enumerate(results, 1):
    print(f"{i}. {id} - {brand} - {model} - {issue} (Distance: {distance:.4f})")

# Propose a solution
# Version 1
prompt1 = ("You are an assistant who can provide help and advice on how to solve any problems and defects of smartphones."
        "You need to start the chat by summarizing the problem exposed by the user and explain some solutions."
        "You only need to elaborate the following possible solutions and not to give alternative solutions based on your knowledge base."
        "If there are no possible solutions you just need to say that unfortunately you can't give help."
        f"Here the question from the user '{search_query}', here possible solutions:\n"
        f"{'\n'.join(f'- ({brand} {model}): {fix}' for (id, brand, model, issue, fix, distance) in results)}\n")

# Version 2
data = '\n'.join(f'- ({brand} {model}): {fix}' for (id, brand, model, issue, fix, distance) in results)
prompt2 = f"Using this data:\n{data}.\nRespond to this prompt: {search_query}"

response = ollama_client.generate(prompt=prompt1)
print(response)

db.close()
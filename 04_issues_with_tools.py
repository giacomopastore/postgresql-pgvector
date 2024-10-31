from loguru import logger
import os
from dotenv import load_dotenv
from db_client import PostgresClient
from llm_client import OllamaClient, OllamaAsyncClient
from issue_manager import IssueManager
import asyncio
import json

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
ollama_async_client = OllamaAsyncClient(host=ollama_host, model=ollama_model, embed_model=ollama_embed_model)
issue_manager = IssueManager(db, ollama_client)

# Generate embeddings for issues
issues = db.select('issues', columns='id, brand, model, issue', where_clause='issue_embedding IS NULL')
for (id, brand, model, issue) in issues:
    issue_manager.update_issue_embed(id, f"Brand: {brand}, Model: {model}, Issue: {issue}")

def convert_results_to_json(results):
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
    return json.dumps(json_results)

async def run():
    # Serch for similar issues
    messages = [{'role': 'user', 'content': "I'm not able to hear audio during call from my iphone"}]

    # First API call: Send the query and function description to the model
    response = await ollama_async_client.chat(
        messages=messages,
        tools=[
            {
                'type': 'function',
                'function': {
                'name': 'issue_manager.search_similar_issues',
                'description': "Search for issues similar to the user's",
                'parameters': {
                    'type': "object",
                    'properties': {
                    'query': {
                        'type': "string",
                        'description': "User question",
                    }
                    },
                    'required': ['query'],
                },
                },
            },
        ],
    )

    # Add the model's response to the conversation history
    messages.append(response['message'])

    # Check if the model decided to use the provided function
    if not response['message'].get('tool_calls'):
        print("The model didn't use the function. Its response was:")
        print(response['message']['content'])

    # Process function calls made by the model
    if response['message'].get('tool_calls'):
        available_functions = {
            'issue_manager.search_similar_issues': issue_manager.search_similar_issues,
        }
        for tool in response['message']['tool_calls']:
            function_to_call = available_functions[tool['function']['name']]
            function_response = function_to_call(tool['function']['arguments']['query'])
            # Add function response to the conversation
            messages.append(
            {
                'role': 'tool',
                'content': convert_results_to_json(function_response),
            }
        )

    # Second API call: Get final response from the model
    for part in ollama_client.chat(messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)

# Run the async function
asyncio.run(run())
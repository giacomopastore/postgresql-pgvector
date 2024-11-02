import sys
import os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from loguru import logger
from dotenv import load_dotenv
from db_client import PostgresClient
from llm_client import OllamaClient, OllamaAsyncClient
from issue_manager import IssueManager
import asyncio
import json
from flask import Flask, render_template, request

app = Flask(__name__)

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
#issues = db.select('issues', columns='id, brand, model, issue', where_clause='issue_embedding IS NULL')
#for (id, brand, model, issue) in issues:
#    issue_manager.update_issue_embed(id, f"Brand: {brand}, Model: {model}, Issue: {issue}")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/answer", methods=["GET", "POST"])
def answer():
    data = request.get_json()
    message = data["message"]

    def generate():
        # Serch for similar issues
        messages = [{'role': 'user', 'content': message}]

        # First API call: Send the query and function description to the model
        response = ollama_client.chat(
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
            logger.info("The model didn't use the function. Its response was:")
            logger.debug(json.dumps(response['message']['content'], indent=4))

        # Process function calls made by the model
        if response['message'].get('tool_calls'):
            available_functions = {
                'issue_manager.search_similar_issues': issue_manager.search_similar_issues,
            }
            for tool in response['message']['tool_calls']:
                function_to_call = available_functions[tool['function']['name']]
                function_response = function_to_call(tool['function']['arguments']['query'])
                logger.info(f"The model used the function {function_to_call}")
                logger.debug(f"Its response was: {json.dumps(function_response, indent=4)}")
                # Add function response to the conversation
                messages.append(
                {
                    'role': 'tool',
                    'content': json.dumps(function_response),
                }
            )

        messages.append({'role': 'user', 'content': 'List similar problems found previously with function issue_manager.search_similar_issues in a table saying: Here are the similar issues I found: \
                         Then explain to the user how to fix the issues on the basis of previous results. \
                         Do not refer to external knowledge base'})
        
        # Second API call: Get final response from the model
        for part in ollama_client.chat(messages=messages, stream=True):
            yield(part['message']['content'])

    return generate(), {"Content-Type": "text/plain"}

if __name__ == '__main__':
    app.run(debug=True)
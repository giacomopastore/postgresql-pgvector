from loguru import logger
import os
from dotenv import load_dotenv
from db_client import PostgresClient
from llm_client import OllamaClient, OllamaAsyncClient
from issue_manager import IssueManager
import asyncio
import json
import cmd

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

async def run(query: str):
    # Serch for similar issues
    messages = [{'role': 'user', 'content': query}]

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
                'content': json.dumps(function_response),
            }
        )

    #messages.append({'role': 'user', 'content': 'List the similar issues, one issue per line \
    #                 by including these fiels: brand, model, issue, distance and then give an explanation on \
    #                 how to solve the problem based on the similar issues'})

    #messages.append({'role': 'user', 'content': 'Explain to the user how to fix the issues and also put references to similar problems found.'})
    
    # Second API call: Get final response from the model
    for part in ollama_client.chat(messages=messages, stream=True):
        print(part['message']['content'], end='', flush=True)

class MyChat(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to MyCLI"
    
    def default(self, line):
        if line:
            try:
                asyncio.run(run(line))
            except Exception as e:
                logger.error(f"Error on MyChat: {e}")
                return None
            
    def emptyline(self):
        pass

    
if __name__ == "__main__":    
    #asyncio.run(main())
    MyChat().cmdloop()
import os
from dotenv import load_dotenv
import psycopg2
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

ollama_client = Client(host=ollama_host)

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# Create a table for our documents
cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(768)
    )
""")

# Get embeddings from Ollama
def get_embedding(text):
    response = ollama_client.embed(model=ollama_embed_model, input=text)    
    return ",".join(map(str, response['embeddings']))

# Add document to DB
def add_document(content):
    embedding = get_embedding(content)    
    cur.execute("INSERT INTO documents (content, embedding) VALUES (%s, %s)", (content, embedding))
    conn.commit()

# Search for similar documents
def search_documents(query, limit=5):
    query_embedding = get_embedding(query)
    cur.execute("""
        SELECT content, embedding <-> %s::vector(768) AS distance
        FROM documents
        ORDER BY distance
        LIMIT %s
    """, (query_embedding, limit))
    return cur.fetchall()

# Add some sample documents
documents = [
  "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
  "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
  "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
  "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
  "Llamas are vegetarians and have very efficient digestive systems",
  "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
]
for doc in documents:
    add_document(doc)

# Perform a search
#search_query = "What animals are llamas related to?"
search_query = "How much does a llama weigh?"
results = search_documents(search_query)
print(f"Search results for: '{search_query}'")
for i, (content, distance) in enumerate(results, 1):
    print(f"{i}. {content} (Distance: {distance:.4f})")

# Generate a response combining the prompt and data we retrieved in step before
output = ollama_client.generate(
  model=ollama_model,
  prompt=f"Using this data: {results[0]}. Respond to this prompt: {search_query}"
)
print(output['response'])

# Clean the table
cur.execute("""
    DELETE FROM documents
""")
conn.commit()

# Clean up
cur.close()
conn.close()
 # Introduction

 Taking inspiration from:
 
 - [pgvector Tutorial: Integrate Vector Search into PostgreSQL](https://www.datacamp.com/tutorial/pgvector-tutorial?dc_referrer=https%3A%2F%2Fwww.google.com%2F)
 - [How to run LLM model locally using only Macbook Air M1/M2](https://thaihoang.org/blog/llm-macbook/)
 - [Ollama](https://github.com/ollama/ollama)
 - [Ollama Python Library](https://github.com/ollama/ollama-python)
 - [Embedding models](https://ollama.com/blog/embedding-models)

# PostgreSQL + pgvector

## Docker

- Build the image  
`docker build -t postgres-pgvector .`

- Run the container  
`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password --name my-postgres-pgvector postgres-pgvector`

- Test the container  
`docker exec -it my-postgres-pgvector psql -U postgres`

## pgvector

- Enable the extension: `CREATE EXTENSION vector;`

# Tests

- vnev setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## pgvector test

- Create the table:
```
CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  embedding vector(3)
);
```

- Insert sample data: `INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[1,1,1]');`
- Calculates the Euclidean distance between vectors: `SELECT * FROM items ORDER BY embedding <-> '[2,3,4]' LIMIT 1;`
- Calculates the cosine distance between vectors: `SELECT * FROM items ORDER BY embedding <=> '[2,3,4]' LIMIT 1;`
- Create IVFFlat index: `CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);`

- Execute [./pgvector_test.py](pgvector_test.py) to test with Python.

## ollama + pgvector test

- Execute [./ollama_pgvector_test.py](ollama_pgvector_test.py) to test.
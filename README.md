 # Introduction

Taking inspiration from:
 
- [pgvector Tutorial: Integrate Vector Search into PostgreSQL](https://www.datacamp.com/tutorial/pgvector-tutorial?dc_referrer=https%3A%2F%2Fwww.google.com%2F)
- [How to run LLM model locally using only Macbook Air M1/M2](https://thaihoang.org/blog/llm-macbook/)
- [Ollama](https://github.com/ollama/ollama)
- [Ollama embedding models](https://ollama.com/blog/embedding-models)
- [Ollama Python Library](https://github.com/ollama/ollama-python)
- [How to get streamed output chunk by chunk using flask api](https://github.com/langchain-ai/langchain/discussions/20124)
- [Flask streaming example](https://github.com/PrettyPrinted/youtube_video_code/blob/master/2024/03/28/How%20to%20Stream%20OpenAI%20API%20Responses%20in%20a%20Flask%20App/README.md)

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

- Execute [./01_pgvector_test.py](01_pgvector_test.py) to test with Python.

## ollama + pgvector test
- Execute [./02_ollama_pgvector_test.py](02_ollama_pgvector_test.py)

# Issues DB
- Execute [./generate_issues_dataset.py](generate_issues_dataset.py) to generate issue records in the DB.

## ollama + pgvector test
- Execute [./03_issues.py](03_issues.py)

## tools + ollama + pgvector test
- Execute [./04_issues_with_tools.py](04_issues_with_tools.py)

## cmdline + tools + ollama + pgvector test
- Execute [./05_issues_with_cmdline.py](05_issues_with_cmdline.py)
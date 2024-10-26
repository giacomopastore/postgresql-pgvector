 # Introduction

 Taking inspiration from [pgvector Tutorial: Integrate Vector Search into PostgreSQL](https://www.datacamp.com/tutorial/pgvector-tutorial?dc_referrer=https%3A%2F%2Fwww.google.com%2F)

# PostgreSQL + pgvector 

## Docker Setup

### Build and run

- Build the image  
`docker build -t postgres-pgvector .`

- Run the container  
`docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password --name my-postgres-pgvector postgres-pgvector`

### Test
`docker exec -it my-postgres-pgvector psql -U postgres`

## pgvector Setup and Test
- Enable the extension
`CREATE EXTENSION vector;`

- Create the table
```
CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  embedding vector(3)
);
```

- Insert sample data  
`INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]'), ('[1,1,1]');`

- Calculates the Euclidean distance between vectors  
`SELECT * FROM items ORDER BY embedding <-> '[2,3,4]' LIMIT 1;`

- Calculates the cosine distance between vectors  
`SELECT * FROM items ORDER BY embedding <=> '[2,3,4]' LIMIT 1;`

- Create IVFFlat index  
`CREATE INDEX ON items USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);`

# Simple test

[./simple_vector_test.py](simple_vector_test.py)

## venv
`python3 -m venv .venv`
`source .venv/bin/activate`
`pip install -r requirements.txt`
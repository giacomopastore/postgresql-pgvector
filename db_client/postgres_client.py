import psycopg2
from psycopg2 import sql

class Postgres:
    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.connection = None
        try:
            self.connection = psycopg2.connect(                                
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            print("Connection to PostgreSQL DB successful")
        except Exception as e:
            print(f"Error connecting to PostgreSQL DB: {e}")

    def select(self, table, columns='*', where_clause=None):
        try:
            query = sql.SQL("SELECT {} FROM {}").format(
                sql.SQL(columns),
                sql.Identifier(table)
            )

            if where_clause:
                query += sql.SQL(" WHERE {}").format(sql.SQL(where_clause))

            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error executing SELECT: {e}")
            return None

    def update(self, table, set_clause, where_clause, params):
        try:            
            query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
                sql.Identifier(table),
                sql.SQL(set_clause),
                sql.SQL(where_clause)
            )

            self.cursor.execute(query, params)
            self.connection.commit()
            print("Update successful")
        except Exception as e:
            print(f"Error executing UPDATE: {e}")
            self.connection.rollback()

    def search_similar_issues(self, query_embedding, limit=5):
        try:    
            self.cursor.execute("""
                SELECT id, issue, issue_embedding <-> %s::vector(768) AS distance
                FROM issues
                ORDER BY distance
                LIMIT %s
            """, (query_embedding, limit))

            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error executing SELECT: {e}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")

if __name__ == '__main__':
    db = Postgres(dbname='your_db', user='your_user', password='your_password')

    results = db.select('your_table', columns='column1, column2', where_clause='column1 = value')
    print(results)

    db.update('your_table', set_clause='column1 = new_value', where_clause='column2 = condition_value')

    db.close()
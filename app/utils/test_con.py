import psycopg
from database import get_connection, execute_query, execute_non_query


def test_connection():
    try:
        conn = get_connection()
        print("Connection successful")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")


def test_query():
    try:
        query = "SELECT * FROM shark_tank_deals"
        result = execute_query(query)
        print(f"Query executed successfully: {result}")
    except psycopg.Error as e:
        print(f"Query execution failed: {e}")


test_query()



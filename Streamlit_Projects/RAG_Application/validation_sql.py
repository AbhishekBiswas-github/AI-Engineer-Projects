# validation_sql.py
from mysql_connection import get_connection
from global_veriables import DATABASE_NAME


def validation_sql(query: str, user_query: str, attempt: int = 1) -> dict:
    """
    Execute the generated SQL query against the database and return a result dict.
    """
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(f"USE {DATABASE_NAME}")
        cursor.execute(query)
        result = cursor.fetchall()
        return {
            "User Query": user_query,
            "Generated Query": query,
            "Result": result,
            "Attempts": attempt,
            "Status": "Success"
        }
    except Exception as e:
        return {
            "User Query": user_query,
            "Generated Query": query,
            "Error": str(e),
            "Attempts": attempt,
            "Status": "Failed"
        }
    finally:
        cursor.close()
        connection.close()

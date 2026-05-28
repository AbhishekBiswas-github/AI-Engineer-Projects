# importing the libraties
from dotenv import load_dotenv
import os
import mysql.connector
import json
from global_veriables import DATABASE_NAME

# loading environment veriable
load_dotenv()

# MySQL Connection
def get_connection():
    """Create and return a new MySQL Connection"""
    return mysql.connector.connect(
        host= os.environ.get("HOST"),
        user= os.environ.get("DB_USER"),
        password = os.environ.get("DATABASE_PASSWORD"),
        port = int(os.environ.get("PORT"))
    )


# re-structuring key types
def key_type_describe(key_type:str) -> str:
    """Map MySQL key type codes to human-readable labels."""
    mapping = {
        "PRI": "PRIMARY KEY",
        "UNI" : "UNIQUE KEY",
        "MUL" : "MULTIPLE KEY"
    }

    return mapping.get(key_type, "None")

# check whether the database present or not
def check_connection(database_name:str) -> str:
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"show databases")
        databases = [database for row in cursor.fetchall() for database in row]
        return "Connected" if database_name in databases else "Database {database_name} Absent"
    except Exception as e:
        return f"Connection Error: {e}"
    finally:
        cursor.close()
        connection.close()

# fetch all the tables from the database
def get_tables(database_name:str) -> list[str]:
    """Fetch all table names from the given database."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(f"Show tables from {database_name}")
        return [table for row in cursor.fetchall() for table in row]
    finally:
        cursor.close()
        connection.close()

# get complete schema of all tables
def get_schemas(database_nane:str, tables:list[str]) -> list[dict]:
    """Fetch full schema details for each table."""
    connection = get_connection()
    cursor = connection.cursor()
    schemans = []

    try: 
        cursor.execute(f"Use {database_nane}")
    
        for table in tables:
            table_schema = {
                'table_name': table,
                'column_details': [],
                'total_records': 0,
                'foreign_key_details': []
            }

            # Geting column details
            cursor.execute(f"DESCRIBE {table}")
            for col in cursor.fetchall():
                table_schema['column_details'].append(
                    f"Column: {col[0]}, Data Type: {col[1]}, Null Constraint: {col[2]}, Key Type: {key_type_describe(col[3])}, Default Value: {col[4]}, Extra Contraints: {col[5]}"
                )

            #   Getting record counts
            cursor.execute(f"select COUNT(*) FROM {table}")
            table_schema["total_records"] =  f"There are {cursor.fetchall()[0][0]} records."

            cursor.execute(f"""SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE REFERENCED_TABLE_NAME IS NOT NULL AND TABLE_NAME = "{table}";
""")
            foreign_key_list = cursor.fetchall()
            if foreign_key_list:
                for col in foreign_key_list:
                    table_schema["foreign_key_details"].append(f"{col[0]}'s table ({col[1]}) column is referencing {col[3]}'s table ({col[4]}) column")
            else:
                table_schema["foreign_key_details"] = "No Relationship exists for this table"

    #         # Returning the schema list
            schemans.append(table_schema)

    finally:
        cursor.close()
        connection.close()
    
    return schemans 

# main mysql function
def get_main_sql(database_name:str = DATABASE_NAME) -> list[dict] | None:
    """Entry point: returns full schema for all tables in the database."""
    
    status = check_connection(database_name)
    if status.lower() == 'connected':
        tables = get_tables(database_name)
        return get_schemas(database_name, tables)
    else:
        print(f"[ERROR] {status}")
        return None






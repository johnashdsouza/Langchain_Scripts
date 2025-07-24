
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.engine import URL
import psycopg2
from smolagents import tool
from typing import List, Dict, Union

def get_engine(user, password, host, port, database):
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=user,
        password=password,
        host=host,
        port=port,
        database=database
    )
    return create_engine(url)


def list_databases(user, password, host, port) -> [str]:
    """
    This tool will get you the list of all databases on the SQL Server Database Server
        Columns:

    Args:
        database_list : A list of strings each containing the name of database on server
    """
    conn = psycopg2.connect(user=user, password=password, host=host, port=port, database="postgres")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
    databases = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return databases

def list_schemas(engine):
    inspector = inspect(engine)
    return inspector.get_schema_names()

@tool
def list_tables(schema: str = 'public') -> List[str]:
    """
    This is a tool that returns the a list of tables in the schema

    Args:
        schema: The list of tables in the schema


    """
    TEST_DB_CONFIG = {
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": 5432,
        "database": "postgres"
    }
    engine = get_engine(**TEST_DB_CONFIG)
    inspector = inspect(engine)
    return inspector.get_table_names(schema=schema)

def get_table_metadata(table_name: str, schema: str = 'public') -> Dict[str, Union[List[Dict[str, Union[str, bool]]], List[str]]]:
     """
    This tool will get the technical metadata of a table in the database

    Columns:
        table_name

    Args:
        metadata: The metadata of a column in json structure
    """
     TEST_DB_CONFIG = {
        "user": "postgres",
        "password": "password",
        "host": "localhost",
        "port": 5432,
        "database": "postgres"
    }
     
     engine = get_engine(**TEST_DB_CONFIG)
     metadata = MetaData()
     table = Table(table_name, metadata, autoload_with=engine, schema=schema)
     return {
        "columns": [{ "name": col.name, "type": str(col.type), "nullable": col.nullable } for col in table.columns],
        "primary_key": [key.name for key in table.primary_key.columns],
        "foreign_keys": [
            {
                "column": fk.parent.name,
                "target_table": fk.column.table.name,
                "target_column": fk.column.name
            } for fk in table.foreign_keys
        ]
     }

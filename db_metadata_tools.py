
from sqlalchemy import create_engine, inspect, MetaData, Table
from sqlalchemy.engine import URL
import psycopg2

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

def list_databases(user, password, host, port):
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

def list_tables(engine, schema):
    inspector = inspect(engine)
    return inspector.get_table_names(schema=schema)

def get_table_metadata(engine, table_name, schema=None):
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


import pytest
from sqlalchemy import create_engine
from db_metadata_tools import (
    get_engine, list_databases, list_schemas,
    list_tables, get_table_metadata
)

# Replace with your test credentials
TEST_DB_CONFIG = {
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": 5432,
    "database": "postgres"
}

@pytest.fixture(scope="module")
def engine():
    return get_engine(**TEST_DB_CONFIG)

def test_list_databases():
    dbs = list_databases(
        TEST_DB_CONFIG["user"],
        TEST_DB_CONFIG["password"],
        TEST_DB_CONFIG["host"],
        TEST_DB_CONFIG["port"]
    )
    assert isinstance(dbs, list)
    assert TEST_DB_CONFIG["database"] in dbs

def test_list_schemas(engine):
    schemas = list_schemas(engine)
    assert isinstance(schemas, list)
    assert "public" in schemas

def test_list_tables(engine):
    tables = list_tables(engine, "public")
    assert isinstance(tables, list)

def test_get_table_metadata(engine):
    tables = list_tables(engine, "public")
    if tables:
        metadata = get_table_metadata(engine, tables[0], schema="public")
        assert "columns" in metadata
        assert isinstance(metadata["columns"], list)

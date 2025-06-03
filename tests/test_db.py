import os
import pytest
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table, inspect
from sqlalchemy.orm import sessionmaker

def get_database_url():
    """接続情報からDBのURLを生成する
    """
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE")
    MYSQL_HOST = os.environ.get("MYSQL_HOST")
    MYSQL_USER = os.environ.get("MYSQL_USER")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
    return f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

@pytest.fixture(scope="session")
def engine():
    return create_engine(get_database_url())

@pytest.fixture(scope="session")
def metadata():
    return MetaData()

@pytest.fixture(scope="session")
def test_table(metadata):
    return Table(
        "test_table", metadata,
        Column("id", Integer, primary_key=True, autoincrement=True),
        Column("name", String(50)),
    )

@pytest.fixture(scope="session")
def Session(engine):
    return sessionmaker(bind=engine)

@pytest.fixture(scope="module")
def connection(engine, metadata, test_table):
    conn = engine.connect()
    metadata.create_all(engine)
    yield conn
    metadata.drop_all(engine)
    conn.close()

@pytest.fixture
def session(connection, Session):
    sess = Session(bind=connection)
    try:
        yield sess
        sess.rollback()
    finally:
        sess.close()

def test_connection(connection):
    assert not connection.closed

def test_create_table(connection):
    inspector = inspect(connection)
    tables = inspector.get_table_names()
    assert "test_table" in tables

def test_insert(session, test_table):
    ins = test_table.insert().values(name="Alice")
    session.execute(ins)
    session.flush()
    result = session.execute(test_table.select().where(test_table.c.name == "Alice")).mappings().fetchone()
    assert result is not None
    assert result["name"] == "Alice"

def test_update(session, test_table):
    ins = test_table.insert().values(name="Bob")
    session.execute(ins)
    session.flush()
    upd = test_table.update().where(test_table.c.name == "Bob").values(name="Bobby")
    session.execute(upd)
    session.flush()
    result = session.execute(test_table.select().where(test_table.c.name == "Bobby")).mappings().fetchone()
    assert result is not None
    assert result["name"] == "Bobby"

def test_delete(session, test_table):
    ins = test_table.insert().values(name="Charlie")
    session.execute(ins)
    session.flush()
    delete_stmt = test_table.delete().where(test_table.c.name == "Charlie")
    session.execute(delete_stmt)
    session.flush()
    result = session.execute(test_table.select().where(test_table.c.name == "Charlie")).fetchone()
    assert result is None

def test_select_multiple_rows(session, test_table):
    names = ["Eve", "Frank", "Grace"]
    for name in names:
        session.execute(test_table.insert().values(name=name))
    session.flush()
    results = session.execute(test_table.select()).mappings().fetchall()
    result_names = [row["name"] for row in results]
    for name in names:
        assert name in result_names
    assert len(results) >= 3

def test_select_with_condition(session, test_table):
    session.execute(test_table.insert().values(name="Henry"))
    session.execute(test_table.insert().values(name="Ivy"))
    session.flush()
    result = session.execute(test_table.select().where(test_table.c.name == "Henry")).mappings().fetchone()
    assert result is not None
    assert result["name"] == "Henry"


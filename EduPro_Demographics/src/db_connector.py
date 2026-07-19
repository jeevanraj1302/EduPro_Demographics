"""
EduPro Demographics — Database Connector Module
=================================================
Abstract database connector supporting SQLite (default),
PostgreSQL, and MongoDB. Falls back to Excel when no DB is configured.
"""

import sqlite3
from typing import Optional

import pandas as pd
from loguru import logger

from src.config import DB_TYPE, DB_CONNECTION_STRING, OUTPUT_DIR


# ══════════════════════════════════════════════
# SQLite Operations
# ══════════════════════════════════════════════
def _get_sqlite_path() -> str:
    """Extract SQLite file path from connection string."""
    return DB_CONNECTION_STRING.replace("sqlite:///", "")


def save_to_sqlite(df: pd.DataFrame, table_name: str = "users") -> bool:
    """
    Save DataFrame to SQLite database.

    Parameters
    ----------
    df : pd.DataFrame
        Data to save.
    table_name : str
        Target table name.

    Returns
    -------
    bool
        True if successful.
    """
    try:
        db_path = _get_sqlite_path()
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.close()
        logger.success(f"Saved {len(df):,} records to SQLite ({db_path}).")
        return True
    except Exception as exc:
        logger.error(f"Failed to save to SQLite: {exc}")
        return False


def load_from_sqlite(table_name: str = "users") -> Optional[pd.DataFrame]:
    """
    Load DataFrame from SQLite database.

    Parameters
    ----------
    table_name : str
        Source table name.

    Returns
    -------
    pd.DataFrame or None
        Loaded data, or None on failure.
    """
    try:
        db_path = _get_sqlite_path()
        conn = sqlite3.connect(db_path)
        df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        conn.close()
        logger.success(f"Loaded {len(df):,} records from SQLite.")
        return df
    except Exception as exc:
        logger.warning(f"Could not load from SQLite: {exc}")
        return None


# ══════════════════════════════════════════════
# PostgreSQL Operations
# ══════════════════════════════════════════════
def save_to_postgresql(df: pd.DataFrame, table_name: str = "users") -> bool:
    """Save DataFrame to PostgreSQL. Requires psycopg2."""
    try:
        from sqlalchemy import create_engine
        engine = create_engine(DB_CONNECTION_STRING)
        df.to_sql(table_name, engine, if_exists="replace", index=False)
        logger.success(f"Saved {len(df):,} records to PostgreSQL.")
        return True
    except ImportError:
        logger.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        return False
    except Exception as exc:
        logger.error(f"Failed to save to PostgreSQL: {exc}")
        return False


def load_from_postgresql(table_name: str = "users") -> Optional[pd.DataFrame]:
    """Load DataFrame from PostgreSQL. Requires psycopg2."""
    try:
        from sqlalchemy import create_engine
        engine = create_engine(DB_CONNECTION_STRING)
        df = pd.read_sql(f"SELECT * FROM {table_name}", engine)
        logger.success(f"Loaded {len(df):,} records from PostgreSQL.")
        return df
    except ImportError:
        logger.error("psycopg2 not installed. Run: pip install psycopg2-binary")
        return None
    except Exception as exc:
        logger.warning(f"Could not load from PostgreSQL: {exc}")
        return None


# ══════════════════════════════════════════════
# MongoDB Operations
# ══════════════════════════════════════════════
def save_to_mongodb(df: pd.DataFrame, collection_name: str = "users") -> bool:
    """Save DataFrame to MongoDB. Requires pymongo."""
    try:
        from pymongo import MongoClient
        client = MongoClient(DB_CONNECTION_STRING)
        db = client.get_default_database()
        collection = db[collection_name]
        collection.drop()
        records = df.to_dict("records")
        collection.insert_many(records)
        client.close()
        logger.success(f"Saved {len(df):,} records to MongoDB.")
        return True
    except ImportError:
        logger.error("pymongo not installed. Run: pip install pymongo")
        return False
    except Exception as exc:
        logger.error(f"Failed to save to MongoDB: {exc}")
        return False


def load_from_mongodb(collection_name: str = "users") -> Optional[pd.DataFrame]:
    """Load DataFrame from MongoDB. Requires pymongo."""
    try:
        from pymongo import MongoClient
        client = MongoClient(DB_CONNECTION_STRING)
        db = client.get_default_database()
        collection = db[collection_name]
        records = list(collection.find({}, {"_id": 0}))
        client.close()
        if records:
            df = pd.DataFrame(records)
            logger.success(f"Loaded {len(df):,} records from MongoDB.")
            return df
        return None
    except ImportError:
        logger.error("pymongo not installed. Run: pip install pymongo")
        return None
    except Exception as exc:
        logger.warning(f"Could not load from MongoDB: {exc}")
        return None


# ══════════════════════════════════════════════
# Unified Interface
# ══════════════════════════════════════════════
def save_to_database(df: pd.DataFrame, table_name: str = "users") -> bool:
    """Save data using the configured database type."""
    db_type = DB_TYPE.lower()
    if db_type == "sqlite":
        return save_to_sqlite(df, table_name)
    elif db_type == "postgresql":
        return save_to_postgresql(df, table_name)
    elif db_type == "mongodb":
        return save_to_mongodb(df, table_name)
    else:
        logger.error(f"Unknown DB_TYPE: {db_type}")
        return False


def load_from_database(table_name: str = "users") -> Optional[pd.DataFrame]:
    """Load data using the configured database type."""
    db_type = DB_TYPE.lower()
    if db_type == "sqlite":
        return load_from_sqlite(table_name)
    elif db_type == "postgresql":
        return load_from_postgresql(table_name)
    elif db_type == "mongodb":
        return load_from_mongodb(table_name)
    else:
        logger.error(f"Unknown DB_TYPE: {db_type}")
        return None


def test_connection() -> tuple[bool, str]:
    """
    Test the database connection.

    Returns
    -------
    tuple[bool, str]
        (success, message)
    """
    db_type = DB_TYPE.lower()
    try:
        if db_type == "sqlite":
            db_path = _get_sqlite_path()
            conn = sqlite3.connect(db_path)
            conn.execute("SELECT 1")
            conn.close()
            return True, f"SQLite connection OK ({db_path})"
        elif db_type == "postgresql":
            from sqlalchemy import create_engine
            engine = create_engine(DB_CONNECTION_STRING)
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return True, "PostgreSQL connection OK"
        elif db_type == "mongodb":
            from pymongo import MongoClient
            client = MongoClient(DB_CONNECTION_STRING, serverSelectionTimeoutMS=3000)
            client.admin.command("ping")
            client.close()
            return True, "MongoDB connection OK"
        else:
            return False, f"Unknown DB_TYPE: {db_type}"
    except Exception as exc:
        return False, f"Connection failed: {exc}"

import sqlite3
import time

from sqlite3 import Error

import db_queries


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path, check_same_thread=False)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_multiple_queries(connection, queries):
    cursor = connection.cursor()
    results = []
    for query in queries:
        try:
            cursor.execute(query)
            results.append(cursor.fetchall())
        except Error as e:
            print(f"The error '{e}' occurred")
    connection.commit()
    return results


def save_context(connection, context):
    queries = [
        db_queries.insert_context.format(**context),
        db_queries.get_context.format(**context),
        db_queries.insert_procinfo.format(**context),
    ]
    result = execute_multiple_queries(connection, queries)
    context_id = result[1][0][0]
    return context_id


def save_keystroke(connection, context_id, keyname):
    query = db_queries.insert_keystroke.format(context_id=context_id, keyname=keyname)
    execute_query(connection, query)


def _save_procinfo(connection, context):
    query = db_queries.insert_procinfo.format(**context)
    execute_query(connection, query)


def create_tables(connection):
    execute_query(connection, db_queries.create_contexts_table)
    execute_query(connection, db_queries.create_keystrokes_table)
    execute_query(connection, db_queries.create_procinfo_table)


def insert_dummy_data(connection):
    execute_query(connection, db_queries.insert_dummy_context)
    execute_query(connection, db_queries.insert_dummy_keystrokes)
    execute_query(connection, db_queries.insert_dummy_keystrokes)

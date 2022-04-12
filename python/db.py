import time
import logging

import psycopg

import db_queries

logger = logging.getLogger("ductile.db")


def create_connection(path):
    connection = None
    try:
        connection = psycopg.connect(
            "dbname=keystrokes user=postgres host=localhost port=5432 password=qsczse"
        )
        logger.info("Connection to Postgres DB successful")
    except Exception as e:
        logger.exception(f"Attempted to connect to Postgres DB. Exception: {e}")
    return connection


def execute_query(connection, query, params):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, params)
    except Error as e:
        logger.exception(
            f"Attempted to execute SQL query. Query: {query}. Exception: {e}"
        )
        return
    try:
        result = cursor.fetchall()
    except psycopg.ProgrammingError as e:
        # logger.debug(
        #     f"Attempted to FetchAll in SQL query with no results. Query: {query}. Exception: {e}"
        # )
        pass

    connection.commit()
    return result


def execute_multiple_queries(connection, queries):
    cursor = connection.cursor()
    results = []
    for query, params in queries:
        try:
            cursor.execute(query, params)
        except psycopg.ProgrammingError as e:
            logger.exception(
                f"Attempted to execute multiple SQL queries.  Queries: {queries}  Exception: {e}"
            )
            return
        try:
            result = cursor.fetchall()
        except psycopg.ProgrammingError as e:
            # logger.debug(
            #     f"Attempted to FetchAll in SQL query with no results. Query: {query}. Exception: {e}"
            # )
            results.append([])
            continue
        results.append(result)
    connection.commit()
    return results


def save_context(connection, context):
    insert_context_params = db_queries.make_insert_context_query_params(context)
    get_context_params = db_queries.make_get_context_query_params(context)
    insert_procinfo_params = db_queries.make_insert_procinfo_query_params(context)

    queries = [
        (db_queries.insert_context, insert_context_params),
        (db_queries.get_context, get_context_params),
        (db_queries.insert_procinfo, insert_procinfo_params),
    ]
    result = execute_multiple_queries(connection, queries)
    context_id = result[1][0][0]
    return context_id


def save_keystroke(connection, context_id, keyname):
    params = db_queries.make_insert_keystroke_query_params(context_id, keyname)
    query = db_queries.insert_keystroke
    execute_query(connection, query, params)


def _save_procinfo(connection, context):
    params = db_queries.make_insert_procinfo_query_params(context)
    query = db_queries.insert_procinfo
    execute_query(connection, query, params)


def create_tables(connection):
    execute_query(connection, db_queries.create_contexts_table, [])
    execute_query(connection, db_queries.create_keystrokes_table, [])
    execute_query(connection, db_queries.create_procinfo_table, [])


def insert_dummy_data(connection):
    execute_query(connection, db_queries.insert_dummy_context, [])
    execute_query(connection, db_queries.insert_dummy_keystrokes, [])
    execute_query(connection, db_queries.insert_dummy_keystrokes, [])

from typing import List, Optional
import pandas as pd
import psycopg2.extras
from docassemble.base.util import variables_snapshot_connection, user_info

__all__ = [
    'get_filenames_with_tag', 
    'get_records_from_filename'
]

def get_filenames_with_tag(tag:str) -> List[str]:
    conn = variables_snapshot_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT filename FROM jsonstorage WHERE tag = %(tag)s", {'tag': tag})
    sessions = [record[0] for record in cur]
    conn.close()
    return sessions

def get_records_from_filename(filename:str, tags:Optional[str] = None) -> pd.DataFrame:
    conn = variables_snapshot_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    query = """
    SELECT DISTINCT ON (jsonstorage.key) jsonstorage.data, "user".email 
    FROM jsonstorage 
    LEFT JOIN userdict ON jsonstorage.key = userdict.key 
    LEFT JOIN "user" ON userdict.user_id = "user".id 
    WHERE jsonstorage.filename = %(filename)s
    """

    params = {'filename': filename}

    if tags:
        query += " AND jsonstorage.tag = %(tags)s"
        params['tags'] = tags

    query += " ORDER BY jsonstorage.key"

    cur.execute(query, params)
    records = cur.fetchall()
    df = pd.DataFrame([dict(record['data'], email=record['email']) for record in records])
    conn.close()
    return df
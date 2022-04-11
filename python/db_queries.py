create_keystrokes_table = """
CREATE TABLE IF NOT EXISTS keystrokes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  context_id INTEGER NOT NULL,
  event_timestamp DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
  FOREIGN KEY (context_id) REFERENCES contexts (id)
);
"""

create_procinfo_table = """
CREATE TABLE IF NOT EXISTS procinfos(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  process_id INTEGER NOT NULL,
  thread_id INTEGER NOT NULL,
  context_id INTEGER NOT NULL,
  created_at DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
  UNIQUE (process_id, thread_id, context_id),
  FOREIGN KEY (context_id) REFERENCES contexts (id)
)
"""

create_contexts_table = """
CREATE TABLE IF NOT EXISTS contexts(
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  process_file_name TEXT NOT NULL, 
  process_file_path TEXT NOT NULL, 
  title TEXT NOT NULL,
  UNIQUE(process_file_name, process_file_path, title)
);
"""

get_context = """
SELECT id AS context_id FROM contexts
WHERE contexts.process_file_name = ?
AND contexts.process_file_path = ?
AND contexts.title = ?
;
"""


def make_get_context_query_params(context):
    return [
        context["process_file_name"],
        context["process_file_path"],
        context["title"],
    ]


insert_context = """
INSERT OR IGNORE INTO
  contexts (process_file_name, process_file_path, title)
  VALUES
  (?, ?, ?);
"""


def make_insert_context_query_params(context):
    return [
        context["process_file_name"],
        context["process_file_path"],
        context["title"],
    ]


insert_procinfo = """
INSERT OR IGNORE INTO
  procinfos (process_id, thread_id, context_id)
  SELECT ?, ?, id AS context_id FROM contexts
    WHERE contexts.process_file_name = ?
    AND contexts.process_file_path = ?
    AND contexts.title = ?;
"""


def make_insert_procinfo_query_params(context):
    return [
        context["process_id"],
        context["thread_id"],
        context["process_file_name"],
        context["process_file_path"],
        context["title"],
    ]


insert_keystroke = """
INSERT INTO
  keystrokes (name, context_id)
  VALUES
  (?, ?) 
"""


def make_insert_keystroke_query_params(context_id, keyname):
    return [keyname, context_id]


insert_dummy_context = """
INSERT OR IGNORE INTO
  contexts (process_file_name, process_file_path, title)
  'explorer.exe', '\\Device\\HarddiskVolume3\\Windows\\explorer.exe', 'Extract Compressed (Zipped) Folders';
"""

insert_dummy_keystrokes = """
INSERT INTO
  keystrokes (name, context_id)
VALUES
  ('James', 1),
  ('Leila', 1),
  ('Brigitte', 1),
  ('Mike', 1),
  ('Elizabeth', 1);
"""

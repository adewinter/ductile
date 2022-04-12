create_keystrokes_table = """
CREATE TABLE IF NOT EXISTS keystrokes (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  context_id INTEGER NOT NULL REFERENCES contexts(id),
  event_timestamp timestamp with time zone NOT NULL
   DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);
"""

create_procinfo_table = """
CREATE TABLE IF NOT EXISTS procinfos(
  id BIGSERIAL PRIMARY KEY,
  process_id INTEGER NOT NULL,
  thread_id INTEGER NOT NULL,
  context_id INTEGER NOT NULL REFERENCES contexts(id),
  created_at timestamp with time zone NOT NULL
   DEFAULT (current_timestamp AT TIME ZONE 'UTC'),
  UNIQUE (process_id, thread_id, context_id)
)
"""

create_contexts_table = """
CREATE TABLE IF NOT EXISTS contexts(
  id BIGSERIAL PRIMARY KEY, 
  process_file_name TEXT NOT NULL, 
  process_file_path TEXT NOT NULL, 
  title TEXT NOT NULL,
  UNIQUE(process_file_name, process_file_path, title)
);
"""

get_context = """
SELECT id AS context_id FROM contexts
WHERE contexts.process_file_name = %s
AND contexts.process_file_path = %s
AND contexts.title = %s
;
"""


def make_get_context_query_params(context):
    return [
        context["process_file_name"],
        context["process_file_path"],
        context["title"],
    ]


insert_context = """
INSERT INTO
  contexts (process_file_name, process_file_path, title)
  VALUES
  (%s, %s, %s)
  ON CONFLICT DO NOTHING;
"""


def make_insert_context_query_params(context):
    return [
        context["process_file_name"],
        context["process_file_path"],
        context["title"],
    ]


insert_procinfo = """
INSERT INTO
  procinfos (process_id, thread_id, context_id)
  SELECT %s, %s, id AS context_id FROM contexts
    WHERE contexts.process_file_name = %s
    AND contexts.process_file_path = %s
    AND contexts.title = %s
    ON CONFLICT DO NOTHING;
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
  (%s, %s) 
"""


def make_insert_keystroke_query_params(context_id, keyname):
    return [keyname, context_id]


insert_dummy_context = """
INSERT INTO
  contexts (process_file_name, process_file_path, title)
  'explorer.exe', '\\Device\\HarddiskVolume3\\Windows\\explorer.exe', 'Extract Compressed (Zipped) Folders' ON CONFLICT DO NOTHING;
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

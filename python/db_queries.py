create_keystrokes_table = """
CREATE TABLE IF NOT EXISTS keystrokes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  context_id INTEGER NOT NULL,
  event_timestamp DATETIME DEFAULT(STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
  FOREIGN KEY (context_id) REFERENCES contexts (id)
);
"""


"""
{
    "title": "Extract Compressed (Zipped) Folders",
    "process_id": 6040,
    "thread_id": 3192,
    "process_file_name": "explorer.exe",
    "process_file_path": "\\Device\\HarddiskVolume3\\Windows\\explorer.exe",
    "processed_title": "Extract Compressed (Zipped) Folders",
    "processed_title_hash": "c2fc41e56fd1be55e6c3711490be4231",
    "blob_name": "explorer.exe__c2fc41e56fd1be55e6c3711490be4231.md"
}
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
WHERE contexts.process_file_name = '{process_file_name}'
AND contexts.process_file_path = '{process_file_path}'
AND contexts.title = '{title}'
;
"""

insert_context = """
INSERT OR IGNORE INTO
  contexts (process_file_name, process_file_path, title)
  VALUES
  ('{process_file_name}', '{process_file_path}', '{title}');
"""


insert_procinfo = """
INSERT OR IGNORE INTO
  procinfos (process_id, thread_id, context_id)
  SELECT '{process_id}', '{thread_id}', id AS context_id FROM contexts
    WHERE contexts.process_file_name = '{process_file_name}'
    AND contexts.process_file_path = '{process_file_path}'
    AND contexts.title = '{title}';
"""

insert_keystroke = """
INSERT INTO
  keystrokes (name, context_id)
  VALUES
  ('{keyname}', '{context_id}') 
"""

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

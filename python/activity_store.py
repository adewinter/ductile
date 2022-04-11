import db
import json
import logging


class ActivityStore:
    def __init__(self):
        self.logger = logging.getLogger("ductile.activity_store")
        self.logger.debug("Initializing ActivityStore")
        self.db_connection = db.create_connection("keystrokes.sqlite3")
        self.context_cache = {}

        db.create_tables(self.db_connection)

    def _generate_cache_key_from_context(self, context):
        return f"{context['title']}::{context['process_file_path']}:{context['process_id']}:{context['thread_id']}"

    def _get_context_id(self, context):
        key = self._generate_cache_key_from_context(context)
        if key not in self.context_cache:
            self.logger.debug(f"Saving new cache context: {context}")
            context_id = db.save_context(self.db_connection, context)
            self.context_cache[key] = context_id
        else:
            context_id = self.context_cache[key]

        return context_id

    def save_keyboard_activity(self, keyname, context):
        """
        keyname is a string representing the key that was pressed
        context is information about the key:
            timestamp
            process_id
            window title
            etc
        """
        context_id = self._get_context_id(context)
        db.save_keystroke(self.db_connection, context_id, keyname)

    def save_mouse_activity(self, clickdata, context):
        """
        clickdata contains which mousebutton was pressed
        and pointer coordinates

        context contains info about current window, process_id, etc
        """
        pass

    def shutdown(self):
        self.logger.info("Shutting down ActivityStore.")
        self.db_connection.close()

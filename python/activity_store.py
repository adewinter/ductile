import db
import json


class ActivityStore:
    def __init__(self):
        self.db_connection = db.create_connection("keystrokes.sqlite3")
        self.context_cache = {}

        db.create_tables(self.db_connection)

        # dummy_context = json.loads(example_context)
        # print(dummy_context, "HERE")
        # self.save_keyboard_activity("[CTRL]", dummy_context)
        # self.save_keyboard_activity("[CTRL2]", dummy_context)
        # self.save_keyboard_activity("[CTRL3]", dummy_context)
        # self.shutdown()

    def _generate_cache_key_from_context(self, context):
        return f"{context['title']}::{context['process_file_path']}:{context['process_id']}:{context['thread_id']}"

    def _get_context_id(self, context):
        key = self._generate_cache_key_from_context(context)
        if key not in self.context_cache:
            context_id = db.save_context(self.db_connection, context)
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
        self.db_connection.close()


example_context = '{"title":"Extract Compressed (Zipped) Folders","process_id":6040,"thread_id":3192,"process_file_name":"explorer.exe","process_file_path":"\\\\Device\\\\HarddiskVolume3\\\\Windows\\\\explorer.exe","processed_title":"Extract Compressed (Zipped) Folders","processed_title_hash":"c2fc41e56fd1be55e6c3711490be4231","blob_name":"explorer.exe__c2fc41e56fd1be55e6c3711490be4231.md"}'
if __name__ == "__main__":
    activity_store = ActivityStore()

import keyboard

from blob_store import BlobStore
from config import SAVE_NON_ACTIONABLE_KEYS
from constants import NON_ACTIONABLE_KEYS


class Main:
    def __init__(self):
        self.blob_store = BlobStore()

    def handle_quit(self):
        hotkey = "esc"
        suppress = False
        trigger_on_release = False

        lock = keyboard._Event()

        def keyboardCallback():
            self.blob_store.shutdown()
            lock.set()

        remove = keyboard.add_hotkey(
            hotkey,
            keyboardCallback,
            suppress=suppress,
            trigger_on_release=trigger_on_release,
        )
        lock.wait()
        keyboard.remove_hotkey(remove)

    def handle_key(self, event):
        if event.event_type == "down":
            blob = self.blob_store.get_blob(event)
            if blob:
                blob.save_keystroke(event)


if __name__ == "__main__":
    app = Main()
    keyboard.hook(app.handle_key)
    app.handle_quit()

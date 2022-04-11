import logging

# Configure root logger to log to file and to console
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
fh = logging.FileHandler("ductile.log")
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug(f"Ductile Root logger initialized.")


import keyboard

from activity_store import ActivityStore
from util import get_current_window_info


class Ductile:
    def __init__(self):
        self.activity_store = ActivityStore()
        self.logger = logging.getLogger("ductile")
        self._flush_counter = 0
        self._flush_count = 10
        self._debug_log_keys = []

    def handle_quit(self):
        hotkey = "f1"
        suppress = False
        trigger_on_release = False

        lock = keyboard._Event()

        def keyboardCallback():
            self.activity_store.shutdown()
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
            self._flush_counter += 1
            self._debug_log_keys.append(event.name)
            context = get_current_window_info()
            self.activity_store.save_keyboard_activity(event.name, context)
            if self._flush_counter % self._flush_count == 0:
                self.logger.debug(
                    f"Last {self._flush_count} captured events: {']'.join(['[' + x for x in self._debug_log_keys if x != None]) + ']'}"
                )
                self._debug_log_keys = []


if __name__ == "__main__":
    app = Ductile()
    keyboard.hook(app.handle_key)
    app.handle_quit()

import keyboard

from activity_store import ActivityStore
from util import get_current_window_info


class Main:
    def __init__(self):
        self.activity_store = ActivityStore()

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
            context = get_current_window_info()
            self.activity_store.save_keyboard_activity(event.name, context)
            print(event.name, end="", flush=True)


if __name__ == "__main__":
    app = Main()
    keyboard.hook(app.handle_key)
    app.handle_quit()

import keyboard

from blob_store import BlobStore
from config import SAVE_NON_ACTIONABLE_KEYS
from constants import NON_ACTIONABLE_KEYS
import argparse


class Main:
    def __init__(self, data_folder):
        self.blob_store = BlobStore(data_folder)

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


def create_arg_parser():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--data-folder",
        default="data/",
        help="Folder location for storing all data generated by this utility.",
    )
    return parser


if __name__ == "__main__":

    args = create_arg_parser().parse_args()
    print("HERE ARE ARGS:", args)
    app = Main(data_folder=args.data_folder)
    keyboard.hook(app.handle_key)
    app.handle_quit()

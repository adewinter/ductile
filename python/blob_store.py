import hashlib
import os
from pprint import pformat

from config import DEBUG, DEBUG_VERBOSE
from blob import FileBlob
from util import get_actionable_events, get_current_window_info


class BlobStore:
    def __init__(self, data_folder):
        self.active_blobs = {}
        self.data_folder = data_folder
        dirname = os.path.dirname(data_folder)
        if DEBUG:
            print(f"DIRNAME IS: {dirname}")
        os.makedirs(dirname, exist_ok=True)

    def shutdown(self):
        print("Attempting to shutdown all blobs...")
        for name in self.active_blobs:
            blob = self.active_blobs[name]
            print(f"Closing {name}::{blob}...")
            blob.close()

    def generate_blob_name(self, process_info):
        raw_title = process_info["title"]
        processed_title = raw_title.encode("ascii", "ignore").decode("utf-8").strip()
        processed_title = " ".join(processed_title.split())
        process_info["processed_title"] = processed_title
        title_hash = hashlib.md5(processed_title.encode("utf-8")).hexdigest()
        process_info["processed_title_hash"] = title_hash
        base_name = process_info["process_file_name"]
        extension = ".md"

        blob_name = f"{base_name}__{title_hash}{extension}"
        process_info["blob_name"] = blob_name
        return blob_name

    def get_blob(self, event):
        process_info = get_current_window_info()
        if DEBUG and DEBUG_VERBOSE:
            print(f"Process info: \n:{pformat(process_info)}")

        name = self.generate_blob_name(process_info)

        if name in self.active_blobs:
            return self.active_blobs[name]

        # Special case if we haven't created this blob yet and are trying to decide if we should
        if len(get_actionable_events(event)) == 0:
            return None
        blob = FileBlob(name, self.data_folder, process_info)
        self.active_blobs[name] = blob
        return blob

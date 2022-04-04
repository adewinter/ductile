from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer, byref
import ctypes
import os
import hashlib
from pprint import pformat

from config import DEBUG, DEBUG_VERBOSE
from blob import FileBlob
from util import get_actionable_events

PROCESS_QUERY_INFORMATION = 0x0400

Psapi = ctypes.WinDLL("Psapi.dll")
GetProcessImageFileName = Psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = ctypes.wintypes.DWORD

Kernel32 = ctypes.WinDLL("kernel32.dll")
OpenProcess = Kernel32.OpenProcess
OpenProcess.restype = ctypes.wintypes.HANDLE

MAX_PATH = 260


class BlobStore:
    def __init__(self):
        self.active_blobs = {}

    def shutdown(self):
        print("Attempting to shutdown all blobs...")
        for name in self.active_blobs:
            blob = self.active_blobs[name]
            print(f"Closing {name}::{blob}...")
            blob.close()

    def get_current_window_info(self):
        hWnd = windll.user32.GetForegroundWindow()
        length = windll.user32.GetWindowTextLengthW(hWnd)
        window_title_buffer = create_unicode_buffer(length + 1)
        windll.user32.GetWindowTextW(hWnd, window_title_buffer, length + 1)

        process_id = wintypes.DWORD(0)

        thread_id = windll.user32.GetWindowThreadProcessId(hWnd, byref(process_id))
        process_handle = OpenProcess(PROCESS_QUERY_INFORMATION, False, process_id)
        process_file_name = None
        process_file_path_buffer = (ctypes.c_char * MAX_PATH)()
        if process_handle:

            if (
                GetProcessImageFileName(
                    process_handle, process_file_path_buffer, MAX_PATH
                )
                > 0
            ):
                process_file_name = os.path.basename(process_file_path_buffer.value)

        return {
            "title": window_title_buffer.value,
            "process_id": process_id.value,
            "thread_id": thread_id,
            "process_file_name": process_file_name.decode("utf-8"),
            "process_file_path": process_file_path_buffer.value.decode("utf-8"),
        }

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
        process_info = self.get_current_window_info()
        if DEBUG and DEBUG_VERBOSE:
            print(f"Process info: \n:{pformat(process_info)}")

        name = self.generate_blob_name(process_info)

        if name in self.active_blobs:
            return self.active_blobs[name]

        # Special case if we haven't created this blob yet and are trying to decide if we should
        if len(get_actionable_events(event)) == 0:
            return None
        blob = FileBlob(name, process_info)
        self.active_blobs[name] = blob
        return blob

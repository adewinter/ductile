import keyboard
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer, byref
import ctypes
import os

# from time
from pathlib import Path

from constants import NON_ACTIONABLE_KEYS

PROCESS_QUERY_INFORMATION = 0x0400

Psapi = ctypes.WinDLL("Psapi.dll")
GetProcessImageFileName = Psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = ctypes.wintypes.DWORD

Kernel32 = ctypes.WinDLL("kernel32.dll")
OpenProcess = Kernel32.OpenProcess
OpenProcess.restype = ctypes.wintypes.HANDLE
MAX_PATH = 260


class Blob:
    """
    Base class for storing a variable amount of string data.  Typically a blob would wrap a regular text file
    but could actually be anything capable of reading and writing data
    """

    def __init__(self, name):
        self.name = blobName
        self.last_touch = time.time()
        self.is_active = True

    def getAllData(self):
        pass

    def getLastLine(self):
        pass

    def saveString(self, line):
        pass

    def close(self):
        """
        close up whatever needs to be closed and mark self as .is_active = False
        """
        pass


class FileBlob(Blob):
    FILE_BLOB_FOLDER = Path("data/")

    def __init__(self, name):
        super.__init__(name)
        self.FILE_PATH = FILE_BLOB_FOLDER / name
        try:
            self.file = open(self.FILE_PATH, 'r+b')
        except OSError as e:
            print(f"Could not open file {self.FILE_PATH}:", e)
            self.is_active = False

    def checkActiveOrRaise(self):
        if not self.is_active:
            raise Exception(f"This FileBlob is already marked as inactive. File: {self.FILE_PATH}")

    def getAllData(self):
        self.checkActiveOrRaise()
        out = self.file.readlines()
        self.file.seek(0)
        return out

    def saveString(self, line):
        """
        Save the provided string to the end of the file
        """
        self.checkActiveOrRaise()
        self.file.write(line)

    def getLastLine(self):
        """
        Maybe not super efficient but I'll burn that bridge if I get to it
        """
        out = self.file.readlines()[-1]
        self.file.seek(0)
        return out

    def handleBackspaceChar(self):
        """
        If the 'backspace' key is pressed, we need to delete the last character from the file.
        """
        if self.file.tell() == 0

    def close(self):
        self.file.close()
        self.is_active = False


class Main:
    def __init__(self):
        self.captured_data = ""

    def removeLastChar(self):
        size = len(self.captured_data)
        if len(size == 0):
            return
        self.captured_data = self.captured_data[0 : size - 1]

    def addData(self, inputKey):
        if inputKey.name == "backspace":
            self.removeLastChar()
        print(inputKey)

    def getWindowInfo(self):
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
            "process_id": process_id,
            "thread_id": thread_id,
            "process_file_name": process_file_name,
            "process_file_path": process_file_path_buffer.value,
        }

    def handle_key(self, event):
        # print(dir(event))
        # breakpoint()
        # print(
        #     f"event.device:{event.device},event.event_type:{event.event_type},event.is_keypad:{event.is_keypad},event.modifiers:{event.modifiers},event.name:{event.name},event.scan_code:{event.scan_code},event.time:{event.time},event.to_json:{event.to_json}"
        # )
        if event.event_type == "down":
            window_info = self.getWindowInfo()
            if event.name in NON_ACTIONABLE_KEYS:
                print(f"NON TEXT KEY: {event.name}")
            else:
                print(
                    f"[{event.name}][{window_info['process_file_name']}][{window_info['title']}]"
                )


if __name__ == "__main__":
    app = Main()
    keyboard.hook(app.handle_key)
    keyboard.wait("esc")

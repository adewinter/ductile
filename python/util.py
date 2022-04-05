from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer, byref
import ctypes
import os

import keyboard

from constants import NON_ACTIONABLE_KEYS
from config import (
    DEBUG,
    DEBUG_VERBOSE,
    COMPOUND_KEYS,
    SAVE_NON_ACTIONABLE_KEYS,
    SAVE_COMPOUND_KEYS,
)


PROCESS_QUERY_INFORMATION = 0x0400

Psapi = ctypes.WinDLL("Psapi.dll")
GetProcessImageFileName = Psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = ctypes.wintypes.DWORD

Kernel32 = ctypes.WinDLL("kernel32.dll")
OpenProcess = Kernel32.OpenProcess
OpenProcess.restype = ctypes.wintypes.HANDLE

MAX_PATH = 260


def get_actionable_events(event):
    current_pressed_keys = list(keyboard._pressed_events.values())
    num_pressed_keys = len(current_pressed_keys)

    first_key = current_pressed_keys[0]

    if (
        num_pressed_keys > 1
        and (first_key.name in COMPOUND_KEYS)
        and SAVE_COMPOUND_KEYS
    ):
        return current_pressed_keys

    if num_pressed_keys == 2 and first_key.name == "shift":
        return [event]

    if event.name in NON_ACTIONABLE_KEYS and SAVE_NON_ACTIONABLE_KEYS:
        return [event]

    if event.name not in NON_ACTIONABLE_KEYS:
        return [event]

    return []


def get_current_window_info():
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
            GetProcessImageFileName(process_handle, process_file_path_buffer, MAX_PATH)
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

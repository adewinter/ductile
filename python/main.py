import keyboard
from typing import Optional
from ctypes import wintypes, windll, create_unicode_buffer, byref
import ctypes
import wmi
import os

PROCESS_QUERY_INFORMATION = 0x0400

Psapi = ctypes.WinDLL('Psapi.dll')
GetProcessImageFileName = Psapi.GetProcessImageFileNameA
GetProcessImageFileName.restype = ctypes.wintypes.DWORD

Kernel32 = ctypes.WinDLL('kernel32.dll')
OpenProcess = Kernel32.OpenProcess
OpenProcess.restype = ctypes.wintypes.HANDLE
MAX_PATH = 260

def getForegroundWindowTitle() -> Optional[str]:
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    procId = wintypes.DWORD(0)

    threadid = windll.user32.GetWindowThreadProcessId(hWnd, byref(procId))
    hProcess = OpenProcess(PROCESS_QUERY_INFORMATION, False, procId)
    if hProcess:
        ImageFileName = (ctypes.c_char*MAX_PATH)()
        # print(f"IMAGEFILENAME: {ImageFileName}")
        if GetProcessImageFileName(hProcess, ImageFileName, MAX_PATH)>0:
            filename = os.path.basename(ImageFileName.value)
            print(f"FILENAME:{filename}")
    # print(f"threadid: {threadid}, procId:{procId}")
    
    # 1-liner alternative: return buf.value if buf.value else None
    if buf.value:
        return buf.value
    else:
        return None




def something(event):
    if (event.event_type == 'down'):
        print(f"Event:: Window Name:{getForegroundWindowTitle()}, Name:{event.name}, scan_code:{event.scan_code}, time:{event.time}")

keyboard.hook(something)
keyboard.wait('esc')

c = wmi.WMI ()
print(c)
for process in c.Win32_Process ():
  print("hello", process.ProcessId, process.Name)
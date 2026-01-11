# directkeys.py
import ctypes

SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

# Scan codes (keyboard)
LEFT  = 0x1E
RIGHT = 0x20
UP    = 0x11

def press_key(scan_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(0, scan_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def release_key(scan_code):
    extra = ctypes.c_ulong(0)
    ii = Input_I()
    ii.ki = KeyBdInput(0, scan_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

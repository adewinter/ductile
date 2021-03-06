from keyboard import all_modifiers

NON_TEXT_KEYS = all_modifiers | {
    "esc",
    "enter",
    "delete",
    "ctrl",
    "left",
    "up",
    "down",
    "right",
    "space",
    "esc",
    "backspace",
    "enter",
    "tab",
    "enter",
    "scroll lock",
    "print screen",
    "print screen",
    "print screen",
    "insert",
    "pause",
    "caps lock",
    "caps lock",
    "num lock",
    "num lock",
    "space",
    "space",
    "enter",
    "windows",
    # Mac keys
    "windows",
    "windows",
    "ctrl",
    "alt",
    "menu",
    "menu",
    "menu",
    "menu",
    "page down",
    "page up",
    "page down",
    "page up",
    "play/pause media",
    None,
}


NON_ACTIONABLE_KEYS = NON_TEXT_KEYS - {"backspace", "space", "enter"}

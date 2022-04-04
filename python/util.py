import keyboard

from constants import NON_ACTIONABLE_KEYS
from config import (
    DEBUG,
    DEBUG_VERBOSE,
    COMPOUND_KEYS,
    SAVE_NON_ACTIONABLE_KEYS,
    SAVE_COMPOUND_KEYS,
    SAVE_SHIFT_BASED_COMPOUNDS,
)


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

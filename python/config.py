DEBUG = True
DEBUG_VERBOSE = False  # if we're debugging, should we do so LOUDLY?

SAVE_NON_ACTIONABLE_KEYS = False
SAVE_COMPOUND_KEYS = False
COMPOUND_KEYS = [
    "ctrl",
    "alt",
]  # compound/combo keys to save that make use of this key (e.g. "ctrl" is for saving compound keys like "ctrl+s")

STRIP_EXCESS_WHITESPACE_FROM_TITLE = (
    True  # Turns a window title of "  foo    bar " into "foo bar"
)
STRIP_ALL_WHITESPACE_FROM_TITLE = (
    False  # Turns a window title of "  foo bar" into "foobar"
)

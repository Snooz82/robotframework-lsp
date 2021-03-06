import os

LOG_LEVEL = os.getenv("ROBOTFRAMEWORK_DAP_LOG_LEVEL", "0")
LOG_FILENAME = os.getenv("ROBOTFRAMEWORK_DAP_LOG_FILENAME", None)

# Make sure that the log level is an int.
try:
    LOG_LEVEL = int(LOG_LEVEL)
except:
    LOG_LEVEL = 3

DEBUG = LOG_LEVEL > 1

TERMINAL_NONE = "none"
TERMINAL_INTEGRATED = "integrated"
TERMINAL_EXTERNAL = "external"

VALID_TERMINAL_OPTIONS = [TERMINAL_NONE, TERMINAL_INTEGRATED, TERMINAL_EXTERNAL]

# i.e.: set to False only when debugging.
import os
import sys

USE_TIMEOUTS = True
if "GITHUB_WORKFLOW" not in os.environ:
    if "pydevd" in sys.modules:
        USE_TIMEOUTS = False

# If USE_TIMEOUTS is None, this timeout should be used.
NO_TIMEOUT = None

DEFAULT_TIMEOUT = 10


def is_true_in_env(env_key):
    """
    :param str env_key:
    
    :return bool:
        True if the given key is to be considered to have a value which is to be
        considered True and False otherwise.
    """
    return os.getenv(env_key, "") in ("1", "True", "true")


class BaseOptions(object):

    tcp = False
    host = "127.0.0.1"
    port = 1456
    log_file = None
    verbose = 0

    def __init__(self, args=None):
        """
        :param args:
            Instance with options to set (usually args from configparser).
        """
        if args is not None:
            for attr in dir(self):
                if not attr.startswith("_"):
                    if hasattr(args, attr):
                        setattr(self, attr, getattr(args, attr))

from robocorp_ls_core.options import *

from robotframework_ls.impl.robot_lsp_constants import (
    ENV_OPTION_ROBOT_LSP_DEBUG_PROCESS_ENVIRON,
    ENV_OPTION_ROBOT_LSP_DEBUG_MESSAGE_MATCHERS,
)


class Options(BaseOptions):

    DEBUG_MESSAGE_MATCHERS = is_true_in_env(ENV_OPTION_ROBOT_LSP_DEBUG_MESSAGE_MATCHERS)
    DEBUG_PROCESS_ENVIRON = is_true_in_env(ENV_OPTION_ROBOT_LSP_DEBUG_PROCESS_ENVIRON)


class Setup(object):

    # After parsing args it's replaced with the actual setup.
    options = Options()

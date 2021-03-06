# Original work Copyright 2017 Palantir Technologies, Inc. (MIT)
# See ThirdPartyNotices.txt in the project root for license information.
# All modifications Copyright (c) Robocorp Technologies Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http: // www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from robotframework_ls.robotframework_log import get_logger

try:
    import configparser
except ImportError:
    from robotframework_ls.libs_py2.py2_backports import configparser

import os
import sys

log = get_logger(__name__)


class ConfigSource(object):
    """Base class for implementing a config source."""

    def __init__(self, root_path):
        self.root_path = root_path
        self.is_windows = sys.platform == "win32"
        self.xdg_home = os.environ.get(
            "XDG_CONFIG_HOME", os.path.expanduser("~/.config")
        )

    def user_config(self):
        """Return user-level (i.e. home directory) configuration."""
        raise NotImplementedError()

    def project_config(self, document_path):
        """Return project-level (i.e. workspace directory) configuration."""
        raise NotImplementedError()

    @staticmethod
    def read_config_from_files(files):
        config = configparser.RawConfigParser()
        for filename in files:
            if os.path.isfile(filename):
                config.read(filename)

        return config

    @staticmethod
    def parse_config(config, key, options):
        """Parse the config with the given options."""
        conf = {}
        for source, destination, opt_type in options:
            opt_value = _get_opt(config, key, source, opt_type)
            if opt_value is not None:
                _set_opt(conf, destination, opt_value)
        return conf


def _get_opt(config, key, option, opt_type):
    """Get an option from a configparser with the given type."""
    for opt_key in [option, option.replace("-", "_")]:
        if not config.has_option(key, opt_key):
            continue

        if opt_type == bool:
            return config.getboolean(key, opt_key)

        if opt_type == int:
            return config.getint(key, opt_key)

        if opt_type == str:
            return config.get(key, opt_key)

        if opt_type == list:
            return _parse_list_opt(config.get(key, opt_key))

        raise ValueError("Unknown option type: %s" % opt_type)


def _parse_list_opt(string):
    return [s.strip() for s in string.split(",") if s.strip()]


def _set_opt(config_dict, path, value):
    """Set the value in the dictionary at the given path if the value is not None."""
    if value is None:
        return

    if "." not in path:
        config_dict[path] = value
        return

    key, rest = path.split(".", 1)
    if key not in config_dict:
        config_dict[key] = {}

    _set_opt(config_dict[key], rest, value)

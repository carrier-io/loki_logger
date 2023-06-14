#!/usr/bin/python3
# coding=utf-8

#   Copyright 2022 getcarrier.io
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""
    Constants
"""
from os import environ

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class FormatterMethods(StrEnum):
    RE = 'replacer_re'
    ITER = 'replacer_iter'


FORMATTER_METHOD = environ.get('FORMATTER_METHOD', FormatterMethods.RE)
LOG_SECRETS_REPLACER = environ.get('LOG_SECRETS_REPLACER', '***')

LOG_FORMAT = "%(message)s"
LOG_DATE_FORMAT = "%Y.%m.%d %H:%M:%S %Z"

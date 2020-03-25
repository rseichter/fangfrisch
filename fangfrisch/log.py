"""
Copyright © 2020 Ralph Seichter

This file is part of "Fangfrisch".

Fangfrisch is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Fangfrisch is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Fangfrisch. If not, see <https://www.gnu.org/licenses/>.
"""
import logging
import logging.handlers
import os
import sys
from enum import Enum
from enum import unique
from logging import Handler
from logging import Logger
from logging import NOTSET
from logging import WARNING


@unique
class LogHandlerType(Enum):
    CONSOLE = 1
    SYSLOG = 2


# noinspection PyTypeChecker
_handler: Handler = None
# noinspection PyTypeChecker
_logger: Logger = None


def parse_syslog_target(address: str):
    if address.find('/') >= 0:
        return address
    s = address.split(':')
    host = s[0]
    if len(s) > 1:
        port = int(s[1])
    else:
        port = logging.handlers.SYSLOG_UDP_PORT
    tuple_ = (host, port)
    return tuple_


def _create_handler(type_: LogHandlerType, syslog_target: str):
    if type_ == LogHandlerType.SYSLOG:
        a = parse_syslog_target(syslog_target)
        handler = logging.handlers.SysLogHandler(address=a)
        default = r'fangfrisch: %(message)s'
    else:
        handler = logging.StreamHandler()
        default = r'%(levelname)s: %(message)s'
    fmt = os.getenv('LOG_FORMAT', default)
    handler.setFormatter(logging.Formatter(fmt))
    return handler


def init_logger(type_: LogHandlerType, level=NOTSET, address: str = 'localhost') -> Logger:
    global _handler, _logger
    if _handler is None:
        if level == NOTSET:
            level = os.getenv('LOG_LEVEL', WARNING)
        _handler = _create_handler(type_, address)
        _logger = logging.getLogger('fangfrisch')
        _logger.addHandler(_handler)
        _handler.setLevel(level)
        _logger.setLevel(level)
    return _logger


def eprint(*args, **kwargs) -> None:  # pragma: no cover
    print(*args, file=sys.stderr, **kwargs)


def log_debug(*args, **kwargs) -> None:
    global _logger
    _logger.debug(*args, **kwargs)


def log_error(*args, **kwargs) -> None:
    global _logger
    _logger.error(*args, **kwargs)


def log_fatal(*args, **kwargs) -> None:
    global _logger
    _logger.fatal(*args, **kwargs)


def log_exception(*args, **kwargs) -> None:
    global _logger
    _logger.exception(*args, **kwargs)


def log_info(*args, **kwargs) -> None:
    global _logger
    _logger.info(*args, **kwargs)


def log_warning(*args, **kwargs) -> None:
    global _logger
    _logger.warning(*args, **kwargs)

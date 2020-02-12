import logging
import os

level = os.getenv('LOG_LEVEL')
if level:
    logging.basicConfig(level=level.upper())
log = logging.getLogger(__name__)

import logging
import sys

logger = logging.getLogger(__name__)
# Логи выводятся в STDOUT
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

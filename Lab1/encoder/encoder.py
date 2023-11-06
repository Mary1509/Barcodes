"""Module providing a function to encode data in 3/5 Matrix Code."""
import logging

from . import mappings

logger = logging.getLogger(__name__)


def encode(data):
    """Encode data string"""
    logger.info('Start encoding of data: %s', data)
    result = [mappings.START]
    for num in data:
        num_code = mappings.mapping_table[int(num)]
        result.append(num_code)
    result.append(mappings.STOP)
    logger.info('Finished encoding. Result: %s', result)
    return result

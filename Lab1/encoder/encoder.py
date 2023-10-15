import logging

from . import mappings

logger = logging.getLogger(__name__)


def encode(data):
    logger.info(f'Start encoding of data: {data}')
    result = [mappings.start]
    for num in data:
        num_code = mappings.mapping_table[int(num)]
        result.append(num_code)
    result.append(mappings.stop)
    logger.info(f'Finished encoding. Result: {result}')
    return result

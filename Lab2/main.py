"""Python barcode generator (usage)"""
import logging
import datetime

from barcode import Code128
from barcode.writer import ImageWriter
from barcode.errors import BarcodeError
from PIL import Image

date = datetime.datetime.now().date()

logging.basicConfig(filename=f'encoder_{date}.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


if __name__ == '__main__':
    logging.info('Starting tool')
    logging.info('Getting the user input')
    data = input('Enter data string:')
    logging.info('Entered data: %s', data)
    try:
        result_image = Code128(data, writer=ImageWriter())
        result_image.save('result', options={"module_width": 0.4, "module_height": 20})
        img = Image.open('result.png')
        img.show()
    except BarcodeError as e:
        logging.error('Error encoding data: %s', e)
        print(f'Error encoding: {e}')

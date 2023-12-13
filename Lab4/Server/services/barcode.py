"""Python barcode generator (usage)"""
import logging
import datetime

from barcode import Code128
from barcode.writer import ImageWriter
from barcode.errors import BarcodeError
import tkinter as tk
from tkinter import filedialog
import cv2
from pyzbar import pyzbar

date = datetime.datetime.now().date()

logging.basicConfig(filename=f'encoder_{date}.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


class BarcodeService:

    def __init__(self):
        pass

    @staticmethod
    def scan(img_path):

        root = tk.Tk()
        root.withdraw()

        try:
            logging.info('Selected image file at path %s', img_path)
            if img_path is not None:
                image = cv2.imread(img_path)
                barcodes = pyzbar.decode(image)
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    print("Barcode Data:", barcode_data)
                    logging.info("Barcode Data: %s Type: %s", barcode_data, barcode_type)
                    return barcode_data
            else:
                print('Error: No image file')
                return
        except BarcodeError as err:
            logging.error('Error decoding data: %s', err)
            print(f'Error decoding: {err}')

    @staticmethod
    def generate(code):
        try:
            result_image = Code128(code, writer=ImageWriter(format='png'))
            result_image.save('result', options={"module_width": 0.4, "module_height": 20})
        except BarcodeError as e:
            logging.error('Error encoding data: %s', e)
            print(f'Error encoding: {e}')

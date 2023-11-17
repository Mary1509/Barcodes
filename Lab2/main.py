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

from PIL import Image

date = datetime.datetime.now().date()

logging.basicConfig(filename=f'encoder_{date}.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


def scan_barcode_from_image():
    logging.info('Selected file upload option')

    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(title='Select file image', filetypes=[("PNG files", "*.png"),
                                                                                     ("JPEG files", "*.jpeg")])
        logging.info('Selected image file at path %s',file_path)
        if file_path:
            image = cv2.imread(file_path)
            barcodes = pyzbar.decode(image)
            for barcode in barcodes:
                barcode_data = barcode.data.decode("utf-8")
                barcode_type = barcode.type
                print("Barcode Data:", barcode_data)
                logging.info("Barcode Data: %s Type: %s", barcode_data, barcode_type)
        else:
            print('Selection cancelled')
            return
    except BarcodeError as err:
        logging.error('Error decoding data: %s', e)
        print(f'Error decoding: {e}')



def scan_barcode_from_camera():
    logging.info('Selected image scan option')
    print("Webcam turned on. To finish press 'q'")
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3.640)
    video_capture.set(4.480)

    while True:
        _, frame = video_capture.read()
        barcodes = pyzbar.decode(frame)

        for barcode in barcodes:
            barcode_data = barcode.data.decode("utf-8")
            barcode_type = barcode.type
            print("Barcode Data:", barcode_data)
            logging.info("Barcode Data: %s Type: %s", barcode_data, barcode_type)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def encode():
    data = input('Enter data string:')
    logging.info('Entered data: %s', data)
    try:
        result_image = Code128(data, writer=ImageWriter(format='png'))
        result_image.save('result', options={"module_width": 0.4, "module_height": 20})
        img = Image.open('result.png')
        img.show()
    except BarcodeError as e:
        logging.error('Error encoding data: %s', e)
        print(f'Error encoding: {e}')


if __name__ == '__main__':
    logging.info('Starting tool')
    logging.info('Getting the user input')
    while True:
        logging.info('Selecting option')
        opt = -1
        prompt = """Select option:
        1 - Encode data
        2 - Scan barcode from image
        3 - Scan barcode from camera
        4 - Quit\n"""
        opt = input(prompt)

        match int(opt):
            case 1: encode()
            case 2: scan_barcode_from_image()
            case 3: scan_barcode_from_camera()
            case 4: logging.info('Exitings') and exit(0)
            case _: print('No such option')

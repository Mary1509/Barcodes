"""3/5 Matrix Code basic encoder"""
import logging
import datetime
from itertools import cycle

from tkinter import Tk, Canvas
import encoder.encoder as Encoder

date = datetime.datetime.now().date()

logging.basicConfig(filename=f'encoder_{date}.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


def encode(data_arr):
    try:
        return Encoder.encode(data_arr)
    except Exception as err:
        raise EncodingWarning(err) from err


def display_barcode(data_arr, enc_str):
    """Display generated encoded string in form of png file"""
    color = cycle(['white', 'black'])
    w, h = 700, 200
    win = Tk()
    win.geometry('800x400')
    canvas = Canvas(win, width=w, height=h, background='white')
    canvas.pack()
    start_pos = {
        'x': 5,
        'y': 20
    }
    canvas.create_rectangle(tuple(start_pos.values()),(start_pos['x'] + 5, h-20),
                       fill=next(color),
                       width=0)
    start_pos['x'] += 5

    for module in enc_str:
        for el in module:
            if el == 'W':
                canvas.create_rectangle(tuple(start_pos.values()), (start_pos['x'] + 15, h - 20),
                                   fill=next(color),
                                   width=0)
                start_pos['x'] += 15
            else:
                canvas.create_rectangle(tuple(start_pos.values()), (start_pos['x'] + 5, h - 20),
                                   fill=next(color),
                                   width=0)
                start_pos['x'] += 5
        canvas.create_rectangle(
            tuple(start_pos.values()), (start_pos['x'] + 5, h - 20),
                           fill=next(color),
                           width=0)
        start_pos['x'] += 5
    canvas.create_text((start_pos['x'] - 5) / 2, h - 10,
                       text=data_arr,
                       fill='black')
    win.mainloop()


if __name__ == '__main__':
    logging.info('Starting tool')
    logging.info('Getting the user input')
    data = input('Enter data string:')
    while not data.isnumeric() or len(data) > 10:
        logging.error('Got alphabetic values or string length over 10 chars. Data: %s', data)
        logging.info('Getting the user input')
        print('Data must contain only numeric values and contain less than 10 characters.')
        data = input('Enter data string:')
    logging.info('Entered data: %s', data)
    try:
        encoded_string = encode(data)
        display_barcode(data, encoded_string)
    except Exception as e:
        logging.error('Error encoding data: %s', e)
        print(f'Error encoding: {e}')

import sys
from pynput import keyboard
import numpy as np
from time import sleep

from pySerialTransfer import pySerialTransfer as txfer
from PIL import Image

COLS = 14
ROWS = 10


link = None

def epahya2(data, offset):
    
    size_data = len(data) 
    size_shifted = int(size_data/3)
    remainder = bool(size_data%3)


    shifted_array = [0 for i in range(size_shifted+int(remainder))]

    for i in range(size_shifted):
        shifted_array[i] = data[i*3]
        for o in range(1, 3):
            # print(shifted_array, i*3+o)
            shifted_array[i] = int(shifted_array[i] << 8)
            shifted_array[i] += data[i*3+o]
        # print(shifted_array)
    
    if(size_data%3):
        shifted_array[size_shifted] = data[size_shifted*3]
        
        for i in range(1, size_data%3):
            shifted_array[size_shifted] = shifted_array[size_shifted] << 8
            shifted_array[size_shifted] += data[i+((size_shifted*3))]

    print(shifted_array)
    
    size = link.tx_obj(shifted_array, offset)
    
    print("Sending", data, "... size:", size)
    link.send(size)

def on_release2(key):
    if (key == keyboard.KeyCode.from_char('1')):
        epahya2("1")
    if (key == keyboard.KeyCode.from_char('2')):
        epahya2("2")
    if (key == keyboard.KeyCode.from_char('3')):
        epahya2("3")
    
def imageSendingMachine():
    size = COLS, ROWS
    img = Image.open("rainbow.png")
    img_resized = im.resize(size, Image.ANTIALIAS)

def awaitResponse():
    while not link.available():
        if link.status < 0:
            print('ERROR: {}'.format(link.status))

def mainTest1():
    global link

    
    try:
        keyboard_listener = keyboard.Listener(on_release=on_release2)
        keyboard_listener.start()
        link = txfer.SerialTransfer('/dev/ttyACM0')
        awaitResponse()


        cool = [255]*41
        for i in range(0,len(cool),2):
            cool[i] = 100

        while True:
            epahya2([255, 10, 100, 89, 100, 34, 22, 89, 56],0)

            epahya2([255, 10, 100, 89, 100, 34, 22, 89, 56], 3)
            
            awaitResponse()
            
            print("im pretty")
            sleep(0.2)
            print("im ugly")
            print('Response received:')
            response = link.rx_obj(obj_type=list, obj_byte_size=link.bytesRead, list_format='B')
            print(response)
            # for index in range(link.bytesRead):
                # response += str(link.rxBuff[index])
  
    except KeyboardInterrupt:
        print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        link.close()
        sys.exit()

if __name__ == '__main__':
    mainTest1()
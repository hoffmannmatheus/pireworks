# importing the RPi.GPIO modules
import RPi.GPIO as GPIO

# this lets us have a time delay
from time import sleep

# set up GPIO BOARD numbering scheme
GPIO.setmode(GPIO.BOARD)

# set GPIO pin as output
GPIO.setup(29, GPIO.OUT)

# set GPIO pin to high
GPIO.output(29, 1)

GPIO.setup(31, GPIO.OUT)
GPIO.output(31, 1)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33, 1)
GPIO.setup(35, GPIO.OUT)
GPIO.output(35, 1)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37, 1)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, 1)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36, 1)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38, 1)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40, 1)

try:
    # 8 voltage values in binary corresponding to 8 different colors
    RGB = ['000', '001', '010', '011', '100', '101', '110', '111']
    while(True):
        for x in range(len(RGB)):
            value = RGB[x]
            GPIO.output(29, int(value[0]))
            GPIO.output(31, int(value[1]))
            GPIO.output(33, int(value[2]))
            GPIO.output(35, int(value[0]))
            GPIO.output(37, int(value[1]))
            GPIO.output(15, int(value[2]))
            GPIO.output(36, int(value[0]))
            GPIO.output(38, int(value[1]))
            GPIO.output(40, int(value[2]))
            sleep(0.50)  # wait 0.5 seconds
finally:
    # reset every resources that has been set up by this program
    GPIO.cleanup()
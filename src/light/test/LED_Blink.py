# importing the RPi.GPIO modules
import RPi.GPIO as GPIO

# this lets us have a time delay
from time import sleep

# set up GPIO BOARD numbering scheme
GPIO.setmode(GPIO.BOARD)

blinkCnt = 3
count = 0
pin = 7

# set GPIO pin as output
GPIO.setup(pin, GPIO.OUT)

try:
    while count < blinkCnt:
        GPIO.output(pin, True)  # set gpio pin to high
        print("LED ON")
        sleep(3)    # wait 3 seconds
        GPIO.output(pin, False)  # set gpio pin to low
        print("LED OFF")
        sleep(1)   # wait 1 seconds
        count += 1
finally:
    # reset every resources that has been set up by this program
    GPIO.cleanup()

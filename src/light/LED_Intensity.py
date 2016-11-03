# importing the RPi.GPIO modules
import RPi.GPIO as GPIO

# this lets us have a time delay
from time import sleep

# set up GPIO BOARD numbering scheme
GPIO.setmode(GPIO.BOARD)

# set GPIO pin as output
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#  create PWm Instance
white = GPIO.PWM(22, 100)
red = GPIO.PWM(18, 100)

#  start PWM
white.start(0)

#  set PWM pin up with a frequency of 1kHz
#  and set that output to a 100% duty cycle.
red.start(100)

pause_time = 0.02

try:
    while True:
        for i in range(0,101):
            white.ChangeDutyCycle(i) # change duty cycle where 0.0 <= i <= 100.0
            red.ChangeDutyCycle(100-i)
            sleep(pause_time)
        for i in range(100,-1,-1):
            white.ChangeDutyCycle(i)
            red.ChangeDutyCycle(100-i)
            sleep(pause_time) # wait 0.02 seconds
finally:
    #  stop PWM
    white.stop()
    red.stop()
    # reset every resources that has been set up by this program
    GPIO.cleanup()
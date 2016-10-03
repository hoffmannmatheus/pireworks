import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

blinkCount= 3
count = 0
LEDPin = 7
GPIO.setup(LEDPin, GPIO.OUT)

try:
    while count < blinkCount:
        GPIO.output(LEDPin, True)
        print("LED ON")
        sleep(3)
        GPIO.output(LEDPin, False)
        print("LED OFF")
        sleep(1)
        count +=1
finally:
	GPIO.cleanup()

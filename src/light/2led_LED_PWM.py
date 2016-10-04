import RPi.GPIO as GPIO 
from time import sleep  

GPIO.setmode(GPIO.BOARD) 

GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

white = GPIO.PWM(22, 100)   
red = GPIO.PWM(18, 100)   

white.start(0)              
red.start(100)              

pause_time = 0.02         

try:
    while True:
        for i in range(0,101):     
            white.ChangeDutyCycle(i)
            red.ChangeDutyCycle(100-i)
            sleep(pause_time)
        for i in range(100,-1,-1):     
            white.ChangeDutyCycle(i)
            red.ChangeDutyCycle(100-i)
            sleep(pause_time)
finally:
    white.stop()
    red.stop()
    GPIO.cleanup()


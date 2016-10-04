import RPi.GPIO as GPIO 
from time import sleep  

GPIO.setmode(GPIO.BOARD) 

GPIO.setup(22, GPIO.OUT)

red = GPIO.PWM(22, 100)     

red.start(0)             

pause_time = 0.01        

try:
    while True:
        for i in range(100):
            red.ChangeDutyCycle(i)
            sleep(pause_time)
        for i in range(100):
            red.ChangeDutyCycle(100 - i)
            sleep(pause_time)

except KeyboardInterrupt:   
    red.stop()             
    GPIO.cleanup()          

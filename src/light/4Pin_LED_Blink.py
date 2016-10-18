import RPi.GPIO as GPIO
from time import sleep 


GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.OUT)
GPIO.output(29,1)
GPIO.setup(31, GPIO.OUT)
GPIO.output(31,1)
GPIO.setup(33, GPIO.OUT)
GPIO.output(33,1)
GPIO.setup(35, GPIO.OUT)
GPIO.output(35,1)
GPIO.setup(37, GPIO.OUT)
GPIO.output(37,1)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15,1)
GPIO.setup(36, GPIO.OUT)
GPIO.output(36,1)
GPIO.setup(38, GPIO.OUT)
GPIO.output(38,1)
GPIO.setup(40, GPIO.OUT)
GPIO.output(40,1)

try:
    RGB = ['000','001','010','011','100','101','110','111']
    while(True):
        for x in range(len(RGB)):
            value = RGB[x]            
            GPIO.output(29,int(value[0]))
            GPIO.output(31,int(value[1]))
            GPIO.output(33,int(value[2]))
            GPIO.output(35,int(value[0]))
            GPIO.output(37,int(value[1]))
            GPIO.output(15,int(value[2]))
            GPIO.output(36,int(value[0]))
            GPIO.output(38,int(value[1]))
            GPIO.output(40,int(value[2]))
            sleep(0.50)
    
finally:
	GPIO.cleanup()





       
   
        
 



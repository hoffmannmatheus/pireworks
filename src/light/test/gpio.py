import RPi.GPIO as GPIO

class GPIO_Process():
    def __init__(self,value):
	    self.gpio_setup = GPIO_SETUP
	    self.gpio_values = values
		
	def gpio_configure(self):
	#setup GPIO port and configuration
	    GPIO.setmode(GPIO.BOARD)
        for gpio_num in self.gpio_setup:
            GPIO.setup(gpio_num,GPIO.OUT)
            GPIO.output(gpio_num,1)
	
	def gpio_output(self):
	#output signal to led
        for gpio_num in self.gpio_setup:
            GPIO.output(gpio_num,int(self.values[0])
            GPIO.output(gpio_num,int(self.values[1])
            GPIO.output(gpio_num,int(self.values[2])
	
    def gpio_clean(self):
	#clean up gpio signal
		GPIO.cleanup()

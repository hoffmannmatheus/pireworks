from core_audio_old import CoreAudio,GPIO_Process
from time import sleep
import threading

threads=[]
values_list=[]

def gpio(value_lst):
    for value in value_lst:
        gpio=GPIO_Process(value)
        gpio.gpio_configure()
        gpio.gpio_output()
        gpio.gpio_clean()

def clean_value_list():
    values_list=[]


# Create the audio class
audio = CoreAudio()
# Define a function to take the stream output
def CallbackFunction(values):
    """My simple callback function"""
	values_list.append(values)

# Register your callback
audio.register(CallbackFunction)

# Start audio processing
audio.start()

# Reset configuration
audio.stop()
audio.configure()


t1=threading.Thread(target=audio.start,args=())
threads.append(t1)
t2=threading.Thread(target=gpio,args=(value_list)
threads.append(t2)
t3=threading.Thread(target=sleep,args=(0.5))
threads.append(t3)
t4=threading.Thread(target=clean_value_list,args=())
threads.append(t4)


try:
    while True:
        for t in threads:
		    t.setDaemon(True)
			t.start()
except KeyboardInterrupt:
    audio.deregister()
    audio.stop()

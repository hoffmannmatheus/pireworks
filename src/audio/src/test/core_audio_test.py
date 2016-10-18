import RPi.GPIO as GPIO
from core_audio_old import CoreAudio
from time import sleep

# Define a function to take the stream output
def CallbackFunction(values):
    """My simple callback function"""
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
        GPIO.output(29,int(values[0]))
        GPIO.output(31,int(values[1]))
        GPIO.output(33,int(values[2]))
        GPIO.output(35,int(values[0]))
        GPIO.output(37,int(values[1]))
        GPIO.output(15,int(values[2]))
        GPIO.output(36,int(values[0]))
        GPIO.output(38,int(values[1]))
        GPIO.output(40,int(values[2]))
    finally:
        GPIO.cleanup()


# Create the audio class
audio = CoreAudio()

# Register your callback
audio.register(CallbackFunction)

# Start audio processing
audio.start()

# Test reconfigure
audio.stop()
audio.configure(trigger_threshold = 100)
audio.start()

# Reset configuration
audio.stop()
audio.configure()
audio.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    audio.deregister()
    audio.stop()

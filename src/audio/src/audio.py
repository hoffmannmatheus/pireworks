from core_audio import CoreAudio
import RPi.GPIO as GPIO

# Define a function to take the list output
def callback_function(values):
    """Audio processing output function"""
    # Map output to colors
    red = values[0]
    green = values[1]
    blue = values[2]

    if red == 1 and green != 1:
        GPIO.output(29, 1)
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        GPIO.output(35, 0)
        GPIO.output(37, 0)
        GPIO.output(15, 0)
        GPIO.output(36, 0)
        GPIO.output(38, 0)
        GPIO.output(40, 0)
    elif green == 1 and blue != 1:
        GPIO.output(29, 1)
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        GPIO.output(15, 0)
        GPIO.output(36, 0)
        GPIO.output(38, 0)
        GPIO.output(40, 0)
    elif blue == 1:
        GPIO.output(29, 1)
        GPIO.output(31, 0)
        GPIO.output(33, 0)
        GPIO.output(35, 0)
        GPIO.output(37, 1)
        GPIO.output(15, 0)
        GPIO.output(36, 0)
        GPIO.output(38, 0)
        GPIO.output(40, 1)

# This will create an audio instance to read from the microphone
a = CoreAudio()

# Register your callback
a.register(callback_function)

# Configure audio
a.configure(cutoff_freqs=[800, 2000])

# Setup GPIO pins
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(36, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)

# Start the audio processing, this will spawn a thread for processing
a.start()

# In order to keep the audio thread running, this thread of execution cannot exit
# This call will block until audio exits
a.join()

# Cleanup GPIO pins
GPIO.cleanup()

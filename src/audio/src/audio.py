from core_audio import CoreAudio
import RPi.GPIO as GPIO
from neopixel import *


# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
#		time.sleep(wait_ms/1000.0)



# Define a function to take the list output
def callback_function(values):
    """Audio processing output function"""
    # Map output to colors
    red = values[0]
    green = values[1]
    blue = values[2]
    teal = values[3]
    purple = values[4]
    aquamarine = values[5]
    indigo = values[6]
    blueviolet = values[7]
    pink = values[8]
    springgreen = values[9]

    

    if red == 1 and green != 1:
        colorWipe(strip, Color(0, 255, 0))
    elif green == 1 and blue != 1:
        colorWipe(strip, Color(255, 0, 0))
    elif blue == 1 and teal!=1:
        colorWipe(strip, Color(0, 0, 255))
    elif teal == 1 and purple!=1:
        colorWipe(strip, Color(128, 0, 128))
    elif purple==1 and aquamarine!=1:
        colorWipe(strip, Color(0,128,128))
    elif aquamarine==1 and indigo!=1:
        colorWipe(strip, Color(255,127,212))
    elif indigo==1 and blueviolet!=1:
        colorWipe(strip, Color(0,55,155))
    elif blueviolet==1 and pink !=1:
        colorWipe(strip, Color(0,55,55))
    elif pink==1 and springgreen !=1:
        colorWipe(strip, Color(0,120,30))
    elif springgreen ==1:
        colorWipe(strip, Color(200,50,50))

# This will create an audio instance to read from the microphone
a = CoreAudio()

# Register your callback
a.register(callback_function)

# Configure audio
a.configure(cutoff_freqs=[300,500,800,1000,1300,1500,1800,2000,2300,2800])


# Start the audio processing, this will spawn a thread for processing
a.start()

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
# Intialize the library (must be called once before other functions).
strip.begin()

# In order to keep the audio thread running, this thread of execution cannot exit
# This call will block until audio exits
a.join()


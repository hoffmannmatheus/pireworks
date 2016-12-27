from neopixel import *

# LED strip configuration:
LED_COUNT = 150      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (0-14)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using voltage level shifter)
LED_INVERT = False
COLOR_MAP={'red':(0, 255, 0),'green':(255, 0, 0),'blue':(0, 0, 255),'teal':(128, 0, 128),'purple':(0,128,128),'aquamarine':(255,127,212),'indigo':(0,55,155),'blueviolet':(0,55,55),'pink':(0,120,30),'springgreen':(200,50,50)}
COLOR_SEQUENCE=['red','green','blue','teal','purple','aquamarine','indigo','blueviolet','pink','springgreen']

class LightInput():

    strip = None

    def __init__(self,
                 led_count=LED_COUNT,
                 led_pin=LED_PIN,
                 led_freq=LED_FREQ_HZ,
                 led_dma=LED_DMA,
                 led_brightness=LED_BRIGHTNESS,
                 led_invert=LED_INVERT,
                 color_map=COLOR_MAP,
                 color_seq=COLOR_SEQUENCE):
        self.LED_COUNT = led_count
        self.LED_PIN = led_pin
        self.LED_FREQ_HZ = led_freq
        self.LED_DMA = led_dma
        self.LED_BRIGHTNESS = led_brightness
        self.LED_INVERT = led_invert
        self.COLOR_MAP=color_map
        self.COLOR_SEQUENCE=color_seq

    def colorWipe(self, color):
        """Wipe color across display a pixel at a time."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, color)
            self.strip.show()

    def colorMap(self, values):
        # Map output to colors

        for index in range(len(values)):
            try:
                if values[index]==1 and values[index+1]==0:
                    sequence=COLOR_MAP[self.COLOR_SEQUENCE[index]]
                    self.colorWipe(Color(sequence[0],sequence[1],sequence[2]))
            except:
                sequence=COLOR_MAP[self.COLOR_SEQUENCE[-1]]
                self.colorWipe(Color(sequence[0],sequence[1],sequence[2]))

    def startStrip(self):
        self.strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT,           self.LED_BRIGHTNESS)
        self.strip.begin()

    def setColorSequence(self, sequence):
        self.COLOR_SEQUENCE = sequence

        print("Color Sequence: ", self.COLOR_SEQUENCE)

from neopixel import *

# LED strip configuration:
LED_COUNT = 50      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
COLOR_MAP={'red':(0, 255, 0),'green':(255, 0, 0),'blue':(0, 0, 255),'teal':(128, 0, 128),'purple':(0,128,128),'aquamarine':(255,127,212),'indigo':(0,55,155),'blueviolet':(0,55,55),'pink':(0,120,30),'springgreen':(200,50,50)}
COLOR_SEQUENCE=['red','green','blue','teal','purple','aquamarine','indigo','blueviolet','pink','springgreen']


class LightInput():

    def __init__(self,
                 LED_COUNT,
                 LED_PIN,
                 LED_FREQ_HZ,
                 LED_DMA,
                 LED_BRIGHTNESS,
                 LED_INVERT
                 COLOR_MAP
                 COLOR_SEQUENCE):
        self.LED_COUNT = LED_COUNT
        self.LED_PIN = LED_PIN
        self.LED_FREQ_HZ = LED_FREQ_HZ
        self.LED_DMA = LED_DMA
        self.LED_BRIGHTNESS = LED_BRIGHTNESS
        self.LED_INVERT = LED_INVERT
        self.COLOR_MAP=COLOR_MAP
        self.COLOR_SEQUENCE=COLOR_SEQUENCE

    def colorWipe(self,strip,color):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()


    def colorMap(self,strip,values)
        # Map output to colors

        for index in range(len(values)):
            try:
                if values[index]==1 and values[index+1]==0:
                    sequence=COLOR_MAP[self.COLOR_SEQUENCE[index]]
                    colorWipe(strip,Color(sequence[0],sequence[1],sequence[2]))
            except:
                sequence=COLOR_MAP[self.COLOR_SEQUENCE[-1]]
                colorWipe(strip,Color(sequence[0],sequence[1],sequence[2]))

    def startStrip(self)
        strip = Adafruit_NeoPixel(self.LED_COUNT, self.LED_PIN, self.LED_FREQ_HZ, self.LED_DMA, self.LED_INVERT, self.LED_BRIGHTNESS)
        strip.begin()
        colorMap(strip,values)
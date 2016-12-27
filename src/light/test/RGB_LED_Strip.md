# RGB LED Strip
- Addressable RGB LED strip
- Current draw and voltage drop
- LED strip chaining
- ws281X
  * Pin configuration
  * Composition of 24 bit data
  * Schematic
  * Typical circuit example
- Adafruit Neopixel Library
  * Overview
  * Frequency calculation for N pixels
  * Library functions

## Addressable RGB LED strip

It is 5-meter long strip contains 150 RGB LEDs that can be individually addressed using a one-wire interface,
allowing you full control over the color of each RGB LED.
Each LED strip has three connection points: the input connector, the auxiliary power wires, and the output connector.

![i/p - o/p connectors](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_ip_op-1.png)

The input connector has three male pins inside of a plastic connector shroud,
the auxiliary power wires are connected to the input side of the LED strip and consist of stripped black and red wires.
This provides an alternate (and possibly more convenient) connection point for LED strip power.
The output connector is on the other end of the strip and is designed to mate with the input connector of another
LED strip to allow LED strips to be chained.

![gnd,input,power and aux cables](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_ip_op_aux-2.png)
The black wire is ground, the green wire is the signal input, and the red wire is the power line.

## Current draw and voltage drop

Each RGB LED draws approximately 50 mA when it is set to full brightness and powered at 5 V.
There is some resistance in the power connections between the LEDs, which means that the power voltage near the end of the strip will
be less than the voltage at the start of the LED strip. As the voltage drops, RGB LEDs tend to look redder and draw less current.
This voltage drop is proportional to the current through the strip, so it increases when the LEDs are set to a higher brightness.

## LED strip chaining

Multiple LED strips can be chained together by connecting input connectors to output connectors.
When strips are chained this way, they can be controlled and powered as one continuous strip.
However, as chains get longer, the ends will get dimmer and redder due to the voltage drop across the strip.
If this becomes an issue, you can chain the data lines while separately powering shorter subsections of the chain.
![chaining](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_chaining.png)

## ws281X :

**Pin configuration**

VDD - Power supply LED

DOUT - Control data signal output

VSS - Ground

DIN - Control data signal input

**Composition of 24 bit data**

Red - 1.8-2.2 V ; 620-630 nm

Green - 3.0-3.2 ; 515-513 nm

Blue - 3.0-3.4 V ; 465-475 nm

![pin cofig,24 bit data comp](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_pin%20config_24%20bit%20comp.png)

**Schematic**
![schemativ](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_schem.png)

**Typical circuit example**
![circuit](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/neopix_circuit.png)

## Adafruit Neopixel Library

**Overview**

WS281X LEDs are generally driven at 5V, which requires that the data signal be at the same level. Converting the output from a Raspberry Pi GPIO/PWM to a higher voltage through a level shifter is required.

NeoPixels powered by 5v require a 5V data signal.A level shifter such as a 74AHCT125 or 74HCT245 is used.The longer a wire is,
the more resistance it has. The more resistance, the more voltage drops along its length. If voltage drops too far,
the color of NeoPixels can be affected.

**Frequency calculation for N pixels**

NeoPixels receive data from a fixed-frequency 800 KHz datastream. Each bit of data therefore requires 1/800,000 sec — 1.25 microseconds. One pixel requires 24 bits (8 bits each for red, green blue) — 30 microseconds. After the last pixel’s worth of data is issued, the stream must stop for at least 50 microseconds for the new colors to “latch.”
For a strip of 150 pixels, that’s (150 * 30) + 50, or 4550 microseconds. 1,000,000 / 4550 = 220 updates per second approximately.

**Library functions**

```python
strip.begin()
```
prepares the data pin for NeoPixel output

```python
strip.show()
```
pushes data out to the pixels.since no colors have been set yet,this initializes all the NeoPixels to an initial “off”

```python
strip.setPixelColor(11, 54, 0, 255)
```
n is pixel no. along the strip. pixel color is expressed as red, green and blue brightness levels.
0 is the lowest intensity and 255 is the highest intensity.

```python
Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
```
Adafruit_NeoPixel object

```python
# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


# Define function which animates LEDs.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
```

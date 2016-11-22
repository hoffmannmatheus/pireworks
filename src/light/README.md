# Light Module
- Overview
- Hardware
- RPi GPIO
  * Features
- GPIO PWM

## Overview

The light module transforms the light codes into actual signals to the light devices.


## Hardware

Development & Target hardware is the Raspberry Pi 3 Model B. RGB led lights and simple electronic prototyping tools (eg. breadboards,resistors,jumper cables) will also be needed, but can emulate during development.

Hardware for LED Strip:

- WS2812 LED Strip (with 1 pin for 5V DC, 1 pin for data and 1 pin for ground)
- A breadboard, Jumper Wires(Male to Male and Female to Female)
- A level shifter to convert the 3.3V to 5V
- A power supply, Power jack, 

**OS** : Raspbian

**Tools / Software** : IDLE for python, Fritzing for breadboard layout and PCB Schematic, WS281X Library

http://fritzing.org/home/

https://www.python.org/downloads/

## Rpi.GPIO 
https://pythonhosted.org/RPIO/index.html

https://sourceforge.net/projects/raspberry-gpio-python/

RPi.GPIO module is the driving force behind our Python examples. This set of Python files and source is included with Raspbian, so assuming you’re running that most popular Linux distribution, you don’t need to download anything to get started.

RPIO is an advanced GPIO module for the Raspberry Pi. PWM via DMA (up to 1µs resolution) GPIO input and output (drop-in replacement for RPi.GPIO) GPIO interrupts (callbacks when events occur on input gpios) TCP socket interrupts (callbacks when tcp socket clients send data)
RPIO consists of two main components:

- RPIO – Python modules which you can import in Python 2 or 3.
- rpio – command-line tools for inspecting and manipulating GPIOs system-wide.

Features :

- PWM via DMA (up to 1µs resolution)
- GPIO input and output (drop-in replacement for RPi.GPIO)
- GPIO interrupts (callbacks when events occur on input gpios)
- TCP socket interrupts (callbacks when tcp socket clients send data)
- Command-line tools rpio and rpio-curses
- Well documented, fast source code with minimal CPU usage
- Open source (LGPLv3+)

In order to us RPi.GPIO throughout the rest of your Python script, you need to put this statement at the top of your file:

```python
import RPi.GPIO as GPIO
```

The method `sleep()` suspends execution for the given number of seconds.

```python
# this lets us have a time delay`
from time import sleep
```

After you’ve included the RPi.GPIO module, the next step is to determine which of the two pin-numbering schemes you want to use:

In RPi.GPIO you can use either pin numbers (BOARD) or the Broadcom GPIO numbers (BCM)


```python
# set up GPIO BOARD numbering
GPIO.Setmode(GPIO.BOARD)
```
 
1. `GPIO.BOARD` -  Board numbering scheme. This option specifies that you are referring to the pins by the number of the pin the plug. That means, the numbers printed on the board.

2. `GPIO.BCM` -  Broadcom chip-specific pin numbers. These pin numbers follow the lower-level numbering system defined by the Raspberry Pi’s Broadcom-chip brain.these are the numbers after "GPIO" in the rectangles of the below diagrams:

- `GPIO.setup([Port_or_pin], [GPIO.IN, GPIO.OUT])` - To write GPIO port/pin as an input or output

- `GPIO.output([Port_or_pin], [GPIO.LOW, GPIO.HIGH])` - To write GPIO port/pin as an high or low

- `GPIO.input([pin])` - Used to read GPIO input.If a pin is configured as an input, you can use the GPIO.input([pin]) function to read its value. The input()function will return either a True or False indicating whether the pin is HIGH or LOW.

- `GPIO.cleanup()` - To cleanup / reset any resources / channel that your program might have used

## GPIO PWM

PWM is pulse-width modulation. Put simply, this is a signal that is switched between on and off, usually rather quickly.
Duty cycle function is the percentage of time between pulses that the signal is “high” or “On”. So if you have a frequency of 50 Hz and a duty cycle of 50%, it means that every 1/50th (0.02) of a second a new pulse starts and that pulse is switched off half -way through that time period (after 1/100th or 0.01s).

- `GPIO.PWM([pin], [frequency])` - Initialize PWM function. 


- `PWM.Start([duty cycle])` - Function to set an initial value.

`For example:`

`PWM.Start(50)` -set PWM pin up with a frequency of 1kHz, and set that output to a 50% duty cycle.This will set our PWM pin up with a frequency of 1kHz, and set that output to a 50% duty cycle.

To adjust the value of the PWM output, use the pwm.ChangeDutyCycle([duty cycle]) function. [duty cycle] can be any value between 0 (i.e 0%/LOW) and 100 (i.e. 100%/HIGH).

- `PWM.ChangeDutyCycle([duty cycle])` - To adjust the value of the PWM output,[duty cycle] can be any value between 0 (i.e 0%/LOW) and 100 (ie.e 100%/HIGH). 

- `PWM.Stop` - stop PWM

`example`

```python
# set up GPIO BOARD numbering scheme
GPIO.setmode(GPIO.BOARD)

# set GPIO pin as output
GPIO.setup(22, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

#  create PWm Instance
white = GPIO.PWM(22, 100)
red = GPIO.PWM(18, 100)

#  start PWM
white.start(0)

#  set PWM pin up with a frequency of 1kHz
#  and set that output to a 100% duty cycle.
red.start(100)

pause_time = 0.02

try:
    while True:
        for i in range(0,101):
            white.ChangeDutyCycle(i) # change duty cycle where 0.0 <= i <= 100.0
            red.ChangeDutyCycle(100-i)
            sleep(pause_time)
        for i in range(100,-1,-1):
            white.ChangeDutyCycle(i)
            red.ChangeDutyCycle(100-i)
            sleep(pause_time) # wait 0.02 seconds
finally:
    #  stop PWM
    white.stop()
    red.stop()
    # reset every resources that has been set up by this program
    GPIO.cleanup()
```
## WS2812 Strips (Neopixel)

The WS2812 Integrated Light Source or NeoPixel in Adafruit parlance is the latest advance in the quest for a simple, scalable and affordable full-color LED. Red, green and blue LEDs are integrated alongside a driver chip into a tiny surface-mount package controlled through a single wire. They can be used individually, chained into longer strings or assembled into still more interesting form-factors.

## RGB 150-LED Strip

It is 5-meter long strip contains 150 RGB LEDs that can be individually addressed using a one-wire interface, allowing you full control over the color of each RGB LED. The flexible, waterproof strip runs on 5 V and can be chained with additional WS2812B strips to form longer runs or cut apart between each LED for shorter sections.

## Overview

These flexible RGB LED strips are an easy way to add complex lighting effects to a project. Each LED has an integrated driver that allows you to control the color and brightness of each LED independently. The combined LED/driver IC on these strips is the extremely compact WS2812B, which enables higher LED densities. In the strip, you can actually see the integrated driver and the bonding wires connecting it to the green, red, and blue LEDs, which are on at their dimmest setting.

## Background

The BCM2835 in the Raspberry Pi has a PWM module that is well suited to driving individually controllable WS281X LEDs. Using the DMA, PWM FIFO, and serial mode in the PWM, it's possible to control almost any number of WS281X LEDs in a chain connected to the PWM output pin.
This library and test program set the clock rate of the PWM controller to 3X the desired output frequency and creates a bit pattern in RAM from an array of colors where each bit is represented by 3 bits for the PWM controller as follows.

```python
Bit 1 - 1 1 0
Bit 0 - 1 0 0
```


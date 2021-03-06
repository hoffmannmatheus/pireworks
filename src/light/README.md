# Light Module
- Overview
- Hardware
- RPi GPIO
  * Features
- GPIO PWM
- [RGB_LED_Strip](https://github.com/hoffmannmatheus/pireworks/blob/master/src/light/test/RGB_LED_Strip.md)

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

[FRITZING](http://fritzing.org/home/)

[PYTHON](https://www.python.org/downloads/)

## Rpi.GPIO 
[RPIO Documentation](https://pythonhosted.org/RPIO/index.html)

[Raspberri Pi GPIO examples](https://sourceforge.net/projects/raspberry-gpio-python/)

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
#  create PWm Instance
white = GPIO.PWM(22, 100)
red = GPIO.PWM(18, 100)

#  start PWM
white.start(0)
red.start(100) # set PWM pin up with a frequency of 1kHz and set that output to a 100% duty cycle.

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
    white.stop() #  stop PWM
    red.stop()
    GPIO.cleanup() # reset every resources that has been set up by this program    
```

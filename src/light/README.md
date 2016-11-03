# Light Module
## Overview

The light module transforms the light codes into actual signals to the light devices.


## Hardware

Development & Target hardware is the Raspberry Pi 3 Model B. RGB led lights and simple electronic prototyping tools (eg. breadboards,resistors,jumper cables) will also be needed, but can emulate during development.

**OS** : Raspbian

**Tools / Software** : IDLE for python, Fritzing for breadboard layout and PCB Schematic

(http://fritzing.org/home/)

(https://www.python.org/downloads/)

## Rpi.GPIO 


RPi.GPIO module is the driving force behind our Python examples. This set of Python files and source is included with Raspbian, so assuming you’re running that most popular Linux distribution, you don’t need to download anything to get started.

RPIO is an advanced GPIO module for the Raspberry Pi. PWM via DMA (up to 1µs resolution) GPIO input and output (drop-in replacement for RPi.GPIO) GPIO interrupts (callbacks when events occur on input gpios) TCP socket interrupts (callbacks when tcp socket clients send data)
RPIO consists of two main components:

- RPIO – Python modules which you can import in Python 2 or 3 with import RPIO, import RPIO.PWM, etc.
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
 after importing the RPi.GPIO module, we set our GPIO numbering mode.
The method `sleep()` suspends execution for the given number of seconds.

```python
# this lets us have a time delay`
from time import sleep
```

After you’ve included the RPi.GPIO module, the next step is to determine which of the two pin-numbering schemes you want to use:

```python
# set up GPIO BOARD numbering
GPIO.Setmode(GPIO.BOARD)
```

## History

TODO: Write history

## Credits

TODO: Write credits

## License

TODO: Write license

This site was built using [GitHub Pages](https://pages.github.com/).

Use `git status` to list all new or modified files that haven't yet been committed.

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")

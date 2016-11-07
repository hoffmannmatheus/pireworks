#Audio & Light Module Test & Integration 

##Overview
This part of code is for testing and integration with audio and light module.
There are three important files following:

(1)The `mic_test.py` module is for testing microphone.

(2)The `core_audio_test.py` module is for testing the `CoreAudio` class with `audio_sweep.wav`.

(3)The `test.py` module is for testing the integration with audio and light.

Also, we have a [gpio class](https://github.com/hoffmannmatheus/pireworks/tree/master/src/light/gpio.py) defined to make the code more clean and objected oriented.

##Testing Part 1: microphone
`stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
`

Get the audio data from microphone and store to stream.

`data = numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16)`

Formating and starting process the data from microphone.


##Testing Part 2: test integration using `test.py` 
Since we have both `audio code` and `led code` working, we are trying to put the code together and we define the low peak vaule as red, middle peak value as green and high peak value as blue:

`red = lowPeakValue >= TRIGGER_THRESHOLD`

`green = midPeakValue >= TRIGGER_THRESHOLD`

`blue = highPeakValue >= TRIGGER_THRESHOLD`

Then we set up value on the gpio board:
```python
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
```
    
and pass value to be shown with led.

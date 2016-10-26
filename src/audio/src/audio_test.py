import pyaudio
import signal
import sys
import numpy
import RPi.GPIO as GPIO
from time import sleep 



FORMAT = pyaudio.paInt16
CHANNELS = 1
RUN = True

# Make these values configurable!
LOW_BIN_CUTOFF=800
HIGH_BIN_CUTOFF=2000
TRIGGER_THRESHOLD=10000
RATE = 44100
CHUNK = 512

# Setup a signal handler to catch Ctrl+C to exit the program
def signal_handler(signal, frame):
    RUN = False
    sys.exit()

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Open PyAudio
audio = pyaudio.PyAudio()

# Open an audio stream from the mic input
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

while RUN is True:
    # Read audio samples from the audio stream  
    try:
        data = numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16)
    except:
        continue
    # Take the FFT of the data
    fft = numpy.fft.fft(data)
    fftBins = len(fft)

    # Obtain the sample frequencies that correspond to the FFT samples
    freqs = numpy.fft.fftfreq(fftBins)

    # Sort the data based on provided cutoff values
    binResolution = RATE / fftBins

    lowBinIndex = int(LOW_BIN_CUTOFF / binResolution)
    highBinIndex = int(HIGH_BIN_CUTOFF / binResolution)

    # Find the peak frequencies and magnitudes
    lowPeakIndex = numpy.argmax(numpy.abs(fft[1:lowBinIndex]))
    lowPeakValue = numpy.abs(fft[lowPeakIndex])

    midPeakIndex = numpy.argmax(numpy.abs(fft[lowBinIndex + 1:highBinIndex]))
    midPeakValue = numpy.abs(fft[lowBinIndex + 1 + midPeakIndex])

    highPeakIndex = numpy.argmax(numpy.abs(fft[highBinIndex + 1:highBinIndex + 1 + (highBinIndex - lowBinIndex)]))
    highPeakValue = numpy.abs(fft[highBinIndex + 1 + highPeakIndex])

    # Convert the sample frequencies into the actual frequencies
    lowPeakFreq = abs(freqs[lowPeakIndex] * RATE)
    midPeakFreq = abs(freqs[lowBinIndex + midPeakIndex] * RATE)
    highPeakFreq = abs(freqs[highBinIndex + highPeakIndex] * RATE)

    red = lowPeakValue >= TRIGGER_THRESHOLD
    
    green = midPeakValue >= TRIGGER_THRESHOLD
    blue = highPeakValue >= TRIGGER_THRESHOLD
    # This is where to call the light module
    print("%d%d%d" % (red, green, blue))
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

    if red==1 and green !=1:
        GPIO.output(29,1)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(35,0)
        GPIO.output(37,0)
        GPIO.output(15,0)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,0)
    elif green==1 and blue !=1:
        GPIO.output(29,1)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(35,0)
        GPIO.output(37,1)
        GPIO.output(15,0)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,0)
    elif blue==1:
        GPIO.output(29,1)
        GPIO.output(31,0)
        GPIO.output(33,0)
        GPIO.output(35,0)
        GPIO.output(37,1)
        GPIO.output(15,0)
        GPIO.output(36,0)
        GPIO.output(38,0)
        GPIO.output(40,1)
    '''
    elif green==1:

    elif blue==1:
        GPIO.output(36,1)
    '''
    GPIO.cleanup()
    # Debug prints
    #print("- freq -\nlow = %d\nmid = %d\nhigh = %d\n" % (lowPeakFreq, midPeakFreq, highPeakFreq))
    #print("- value -\nlow = %d\nmid = %d\nhigh = %d\n" % (lowPeakValue, midPeakValue, highPeakValue))

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()

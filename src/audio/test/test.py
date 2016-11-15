import pyaudio
import signal
import sys
import numpy
import RPi.GPIO as GPIO
from time import sleep
import light_module


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

#light strip code start here:
    if red==1 and green!=1:
	light_module.start("red")
    elif green==1 and blue!=1:
	light_module.start('green')
    else:
	light_module.start('blue')



# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()

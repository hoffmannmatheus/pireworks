import pyaudio
import signal
import sys
import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 512
RUN = True

# Make these values configurable!
LOW_BIN_CUTOFF=1000
HIGH_BIN_CUTOFF=3000

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
    data = numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16)
    
    # Take the FFT of the data
    fft = numpy.fft.fft(data)
    fftBins = len(fft)

    # Obtain the sample frequencies that correspond to the FFT samples
    freqs = numpy.fft.fftfreq(fftBins)

    # Sort the data based on provided cutoff values
    binResolution = (RATE / 2) / fftBins

    lowBinIndex = int(LOW_BIN_CUTOFF / binResolution)
    highBinIndex = int(HIGH_BIN_CUTOFF / binResolution)

    # Find the peak frequencies (Sample the same number of frequencies per bin)
    lowPeakIndex = numpy.argmax(numpy.abs(fft[:lowBinIndex - 1]))
    midPeakIndex = numpy.argmax(numpy.abs(fft[lowBinIndex:highBinIndex - 1]))
    highPeakIndex = numpy.argmax(numpy.abs(fft[highBinIndex:highBinIndex + (highBinIndex - lowBinIndex)]))

    # Convert the sample frequencies into the actual frequencies
    lowPeakFreq = abs(freqs[lowPeakIndex] * RATE)
    midPeakFreq = abs(freqs[lowBinIndex + midPeakIndex] * RATE)
    highPeakFreq = abs(freqs[highBinIndex + highPeakIndex] * RATE)

    print("low = %d mid = %d high = %d" % (lowPeakFreq, midPeakFreq, highPeakFreq))

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()

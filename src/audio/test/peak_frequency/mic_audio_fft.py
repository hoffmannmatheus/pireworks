import pyaudio
import signal
import sys
import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RUN = True

# Setup a signal handler to catch Ctrl+C to exit the program
def signal_handler(signal, frame):
    RUN = False

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

    # Obtain the sample frequencies that correspond to the FFT samples
    freqs = numpy.fft.fftfreq(len(fft))

    # Find the peak frequency
    peakIndex = numpy.argmax(numpy.abs(fft))

    # Convert the sample frequency into the actual frequency
    peakFreq = abs(freqs[peakIndex] * RATE)

    print(peakFreq)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
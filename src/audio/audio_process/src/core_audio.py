import pyaudio
import signal
import sys
import numpy
from threading import Thread

LOW_BIN_CUTOFF = 800
HIGH_BIN_CUTOFF = 3000
TRIGGER_THRESHOLD = 10000
RATE = 44100
CHUNK = 1024

class AudioInput(Thread):
    """This is the audio input processing thread."""
    def __init__(self, stream, callback, low_cutoff, high_cutoff, trigger_threshold, rate, chunk):
        Thread.__init__(self)
        self.stream = stream
        self.callback = callback
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.trigger_threshold = trigger_threshold
        self.rate = rate
        self.chunk_size = chunk
        self.running = True

    def stop(self):
        """Stop the currently running thread"""
        self.running = False

    def run(self):
        """The thread function"""
        while self.running is True:
            # Read audio samples from the audio stream
            data = numpy.fromstring(self.stream.read(self.chunk_size), dtype=numpy.int16)

            # Take the FFT of the data
            fft = numpy.fft.fft(data)
            fft_bins = len(fft)

            # Sort the data based on provided cutoff values
            bin_resolution = self.rate / fft_bins

            low_bin_index = int(self.low_cutoff / bin_resolution)
            high_bin_index = int(self.high_cutoff / bin_resolution)

            bin_width = high_bin_index - low_bin_index

            # Find the peak frequencies and magnitudes
            low_peak_index = numpy.argmax(numpy.abs(fft[:low_bin_index]))
            low_peak_value = numpy.abs(fft[low_peak_index])

            mid_peak_index = numpy.argmax(numpy.abs(fft[low_bin_index:high_bin_index]))
            mid_peak_value = numpy.abs(fft[low_bin_index + mid_peak_index])

            high_peak_index = numpy.argmax(numpy.abs(fft[high_bin_index:high_bin_index + bin_width]))
            high_peak_value = numpy.abs(fft[high_bin_index + high_peak_index])

            red = low_peak_value >= self.trigger_threshold
            green = mid_peak_value >= self.trigger_threshold
            blue = high_peak_value >= self.trigger_threshold

            self.callback(red, green, blue)

            # Debug prints

            # Obtain the sample frequencies that correspond to the FFT samples
            #freqs = numpy.fft.fftfreq(fft_bins)

            # Convert the sample frequencies into the actual frequencies
            #low_peak_freq = abs(freqs[low_peak_index] * self.rate)
            #mid_peak_freq = abs(freqs[low_bin_index + mid_peak_index] * self.rate)
            #high_peak_freq = abs(freqs[high_bin_index + high_peak_index] * self.rate)

            # Print the output
            #print("%d%d%d" % (red, green, blue))
            #print("- freq -\nlow = %d\nmid = %d\nhigh = %d\n" %
            #     (low_peak_freq, mid_peak_freq, high_peak_freq))
            #print("- value -\nlow = %d\nmid = %d\nhigh = %d\n" %
            #     (low_peak_value, mid_peak_value, high_peak_value))

class CoreAudio():
    """This class controls the audio processing thread

    The order of operations must be as follows:
    1. Create class isinstance
    2. Register your callback function via the register() operation
    3. (Optional) Configure your desired parameters via the configure() operation
    4. Invoke the start() operation

    *Note* If it is desired to re-configure the audio the following operations must be performed:
    1. Invoke the stop() operation
    2. Configure the desired paramters via the configure() operation
    3. Invoke the start() operation
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.run = True
        self.callback = None
        self.low_cutoff = LOW_BIN_CUTOFF
        self.high_cutoff = HIGH_BIN_CUTOFF
        self.trigger_threshold = TRIGGER_THRESHOLD
        self.rate = RATE
        self.chunk_size = CHUNK
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

    def register(self, callback):
        """Register a callback function"""
        self.callback = callback

    def deregister(self):
        """Delete registered callback function"""
        self.callback = None

    def configure(self, 
                  low_cutoff=LOW_BIN_CUTOFF,
                  high_cutoff=HIGH_BIN_CUTOFF,
                  trigger_threshold=TRIGGER_THRESHOLD,
                  rate=RATE,
                  chunk_size=CHUNK):
        """Configure the audio parameters"""
        self.low_cutoff = low_cutoff
        self.high_cutoff = high_cutoff
        self.trigger_threshold = trigger_threshold
        self.rate = rate
        self.chunk_size = chunk_size

    def start(self):
        """Start audio processing"""
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)
        self.thread = AudioInput(self.stream,
                                 self.callback,
                                 self.low_cutoff,
                                 self.high_cutoff,
                                 self.trigger_threshold,
                                 self.rate,
                                 self.chunk_size)
        self.thread.start()

    def stop(self):
        """Stop audio processing"""
        try:
            self.thread.stop()
            self.stream.stop_stream()
            self.stream.close()
        except:
            pass

        self.stream = None
        self.thread = None

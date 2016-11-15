"""The main audio processing module"""
from threading import Thread
import wave
import math
import pyaudio
import scipy
import numpy

# All these values are configurable
# See below for descriptions of these values
CUTOFF_FREQS = [800, 1500, 3000]
TRIGGER_THRESHOLD = 150000
TRIGGER_OFFSET = 150000
SCALED_MAX_VALUE = 255
OUTPUT_BINARY = True
CHUNK = 8192
RATE = 44100

class AudioInput(Thread):
    """The audio input processing thread"""
    def __init__(self,
                 stream,
                 wav,
                 callback,
                 cutoff_freqs,
                 trigger_threshold,
                 trigger_offset,
                 scaled_max_value,
                 rate,
                 chunk,
                 output_binary):
        Thread.__init__(self)
        self.stream = stream
        self.wav = wav
        self.callback = callback
        self.cutoff_freqs = cutoff_freqs
        self.trigger_threshold = trigger_threshold
        self.trigger_offset = trigger_offset
        self.scaled_max_value = scaled_max_value
        self.rate = rate
        self.chunk_size = chunk
        self.output_binary = output_binary
        self.running = True

    def stop(self):
        """Stop the currently running thread"""
        self.running = False

    def process_value(self, fft_value, peak_values):
        """Determine the appropiate output value based on fft output"""
        if fft_value < self.trigger_threshold:
            peak_values.append(0)
        else:
            if self.output_binary is True:
                peak_values.append(1)
            else:
                scaled_max = self.trigger_threshold + self.trigger_offset

                if fft_value < scaled_max:
                    scaled_value = (scaled_max - fft_value) / scaled_max
                    scaled_value *= self.scaled_max_value
                    peak_values.append(math.ceil(scaled_value))
                else:
                    peak_values.append(self.scaled_max_value)

    def run(self):
        """The thread function"""
        while self.running is True:
            if self.wav is None:
                try:
                    # Read audio samples from the audio stream
                    data = scipy.fromstring(self.stream.read(self.chunk_size), dtype=scipy.int16)
                except BufferError:
                    # Buffer errors are not fatal, continue
                    continue
            else:
                # Read audio samples from input file
                if self.wav.tell() >= self.wav.getnframes():
                    self.wav.rewind()

                data = scipy.fromstring(self.wav.readframes(self.chunk_size), dtype=scipy.int16)

            # Take the FFT of the data
            fft = scipy.fft(data)
            fft_bins = len(fft)

            # Bin the data based on provided cutoff values
            bin_resolution = self.rate / fft_bins

            indicies = []
            for freq in self.cutoff_freqs:
                indicies.append(int(freq / bin_resolution))

            # Find the peak frequencies and magnitudes
            peak_values = []
            for index, value in enumerate(indicies):
                fft_index = 0
                if index is 0:
                    fft_index = scipy.argmax(numpy.abs(fft[:value]))
                else:
                    fft_index = scipy.argmax(numpy.abs(fft[indicies[index - 1]:value]))

                fft_value = 0
                if index is 0:
                    fft_value = numpy.abs(fft[fft_index])
                else:
                    fft_value = numpy.abs(fft[indicies[index - 1] + fft_index])

                self.process_value(fft_value, peak_values)

            # The last bin
            upper_bound = int((len(fft) - indicies[-1]) / 2)
            fft_index = scipy.argmax(numpy.abs(fft[indicies[-1]:upper_bound]))
            fft_value = numpy.abs(fft[indicies[-1] + fft_index])

            self.process_value(fft_value, peak_values)

            self.callback(peak_values)

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
    Parameters
    ----------
    file : string
        If a file is present an attempt will be made to open and use as input
    """
    def __init__(self, file=None):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.run = True
        self.callback = None
        self.cutoff_freqs = CUTOFF_FREQS
        self.trigger_threshold = TRIGGER_THRESHOLD
        self.trigger_offset = TRIGGER_OFFSET
        self.scaled_max_value = SCALED_MAX_VALUE
        self.rate = RATE
        self.chunk_size = CHUNK
        self.output_binary = OUTPUT_BINARY
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

        if file != None:
            try:
                self.wave = wave.open(file, 'rb')
            except wave.Error:
                self.wave = None
        else:
            self.wave = None


    def register(self, callback):
        """Register a callback function
        Parameters
        ----------
        callback : function
            The callback function accepting a list of values indicating
            if a signal is present within the given "bin"
        """
        self.callback = callback

    def deregister(self):
        """Delete registered callback function"""
        self.callback = None

    def configure(self,
                  cutoff_freqs=None,
                  trigger_threshold=TRIGGER_THRESHOLD,
                  trigger_offset=TRIGGER_OFFSET,
                  scaled_max_value=SCALED_MAX_VALUE,
                  rate=RATE,
                  chunk_size=CHUNK,
                  output_binary=True):
        """Configure the audio parameters
        Parameters
        ----------
        cutoff_freqs : list of int
            A list of frequences to divide the input samples.
            Value must be within the range of 20-22,000 Hz
        trigger_threshold : int
            The magnitude of signal needed to produce a "ON" signal
        trigger_offset : int
            The offset to apply to trigger_threshold to determine the scaled output value
        scaled_max_value : int
            The max scaled output value
        rate : int
            The sampling rate in Hz. Modification of this value should
            correspond to hardware configuration changes. Currently only support 44.1 kHz
        chunk_size : int
            The number of samples processed per loop. Only adjust if
            buffer underflows are detected
        output_binary : bool
            Provide output to callback fucntion in binary
        """
        if cutoff_freqs is None:
            cutoff_freqs = CUTOFF_FREQS
        else:
            # Remove duplicates and sort
            cutoff_freqs = sorted(set(cutoff_freqs))

        if max(cutoff_freqs) > 22000:
            raise ValueError("Invalid cutoff frequency, must be below 22000")

        if rate != 44100:
            raise ValueError("Invalid rate frequency, must be 44100")

        self.cutoff_freqs = cutoff_freqs
        self.trigger_threshold = trigger_threshold
        self.scaled_max_value = scaled_max_value
        self.trigger_offset = trigger_offset
        self.rate = rate
        self.chunk_size = chunk_size
        self.output_binary = output_binary

    def start(self):
        """Start audio processing"""
        self.stream = self.audio.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=self.chunk_size)

        self.thread = AudioInput(self.stream,
                                 self.wave,
                                 self.callback,
                                 self.cutoff_freqs,
                                 self.trigger_threshold,
                                 self.trigger_offset,
                                 self.scaled_max_value,
                                 self.rate,
                                 self.chunk_size,
                                 self.output_binary)

        self.thread.start()

    def stop(self):
        """Stop audio processing"""
        if self.thread is not None:
            self.thread.stop()

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()

        self.stream = None
        self.thread = None

    def join(self):
        """Blocks the calling thread until audio exits"""
        self.thread.join()

from threading import Thread
import pyaudio
import numpy

# See below for descriptions of these values
CUTOFF_FREQS = [800, 1500, 3000]
TRIGGER_THRESHOLD = 10000
RATE = 44100
CHUNK = 1024

class AudioInput(Thread):
    """The audio input processing thread"""
    def __init__(self, stream, callback, cutoff_freqs, trigger_threshold, rate, chunk):
        Thread.__init__(self)
        self.stream = stream
        self.callback = callback
        self.cutoff_freqs = cutoff_freqs
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
                    fft_index = numpy.argmax(numpy.abs(fft[:value]))
                else:
                    fft_index = numpy.argmax(numpy.abs(fft[indicies[index - 1]:value]))

                fft_value = 0
                if index is 0:
                    fft_value = numpy.abs(fft[fft_index])
                else:
                    fft_value = numpy.abs(fft[indicies[index - 1] + fft_index])

                if fft_value > self.trigger_threshold:
                    peak_values.append(1)
                else:
                    peak_values.append(0)

            # The last bin
            upper_bound = int((len(fft) - indicies[-1]) / 2)
            fft_index = numpy.argmax(numpy.abs(fft[indicies[-1]:upper_bound]))
            fft_value = numpy.abs(fft[indicies[-1] + fft_index])

            if fft_value > self.trigger_threshold:
                peak_values.append(1)
            else:
                peak_values.append(0)

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
    """
    def __init__(self):
        self.format = pyaudio.paInt16
        self.channels = 1
        self.run = True
        self.callback = None
        self.cutoff_freqs = CUTOFF_FREQS
        self.trigger_threshold = TRIGGER_THRESHOLD
        self.rate = RATE
        self.chunk_size = CHUNK
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.thread = None

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
                  rate=RATE,
                  chunk_size=CHUNK):
        """Configure the audio parameters
        Parameters
        ----------
        cutoff_freqs : list of int
            A list of frequences to divide the input samples.
            Value must be within the range of 20-22,000 Hz
        trigger_threshold : int
            The magnitude of signal needed to produce a "ON" signal
        rate : int
            The sampling rate in Hz. Modification of this value should
            correspond to hardware configuration changes. Currently only support 44.1 kHz
        chunk_size : int
            The number of samples processed per loop. Only adjust if
            buffer underflows are detected.
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
                                 self.cutoff_freqs,
                                 self.trigger_threshold,
                                 self.rate,
                                 self.chunk_size)
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

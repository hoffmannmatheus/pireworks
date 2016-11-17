import pyaudio
import numpy

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 8192

# Open PyAudio
audio = pyaudio.PyAudio()

# Open an audio stream from the mic input
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

history = []

try:
    while True:
        # Read audio samples from the audio stream
        data = numpy.fromstring(stream.read(CHUNK), dtype=numpy.int16)

        # Take the FFT of the data
        fft = numpy.fft.fft(data)
        fft_bins = len(fft)

        # Obtain the sample frequencies that correspond to the FFT samples
        freqs = numpy.fft.fftfreq(fft_bins)

        # Find the peak frequencies and magnitudes
        peak_index = numpy.argmax(numpy.abs(fft))
        peak_value = numpy.abs(fft[peak_index])

        # Convert the sample frequencies into the actual frequencies
        peak_freq = abs(freqs[peak_index] * RATE)

        # Record the peak value
        history.append(peak_value)

        print("The peak frequency is %d with magnitude %d" % (peak_freq, peak_value))
        
except KeyboardInterrupt:
    # Cleanup
    average_peak = int(numpy.average(history))

    print("Recommended Threshold + Recommended Offset = %d" % (average_peak))

    stream.stop_stream()
    stream.close()
    audio.terminate()
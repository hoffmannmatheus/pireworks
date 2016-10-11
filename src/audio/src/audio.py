import pyaudio
import audioop
import matplotlib.pyplot as plt
import numpy as np
from itertools import izip
import wave
import sys

#Read from microphone
'''
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"

audio = pyaudio.PyAudio()

 start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

frames = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
frames = ''.join(frames)

stream.stop_stream()
stream.close()
audio.terminate()

fig = plt.figure()
s = fig.add_subplot(111)
amplitude = numpy.fromstring(frames, numpy.int16)
s.plot(amplitude)
fig.savefig('t.png')
'''


#read from file
CHUNK = 1024

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

wf = wave.open(sys.argv[1], 'rb')

p = pyaudio.PyAudio()


stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)


data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()

p.terminate()

fig = plt.figure()
s = fig.add_subplot(111)
amplitude = np.fromstring(data, np.int16)
s.plot(amplitude)
fig.savefig('pic.png')

import sys
sys.path.append('../src')
from core_audio import CoreAudio
from time import sleep

# Define a function to take the stream output
def callback_function(values):
    """My simple callback function"""
    print(values)

# Create the audio class
#audio = CoreAudio()
audio = CoreAudio("audio_sweep.wav")

# Register your callback
audio.register(callback_function)

# Start audio processing
audio.start()

# Test reconfigure
audio.stop()
audio.configure(output_binary=False)
audio.start()

# Reset configuration
#audio.stop()
#audio.configure()
#audio.start()

try:
    audio.join()
except KeyboardInterrupt:
    audio.deregister()
    audio.stop()

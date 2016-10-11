from core_audio import CoreAudio
from time import sleep

# Define a function to take the stream output
def CallbackFunction(values):
    """My simple callback function"""
    print(values)

# Create the audio class
audio = CoreAudio()

# Register your callback
audio.register(CallbackFunction)

# Start audio processing
audio.start()

# Test reconfigure
audio.stop()
audio.configure(trigger_threshold = 100)
audio.start()

# Reset configuration
audio.stop()
audio.configure()
audio.start()

try:
    while True:
        sleep(1)
except KeyboardInterrupt:
    audio.deregister()
    audio.stop()

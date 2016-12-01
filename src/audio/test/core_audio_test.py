import sys
sys.path.append('../src')
from core_audio import CoreAudio
from time import sleep

# Define a function to take the stream output
def callback_function(values):
    """My simple callback function"""
    print(values)

# Create the audio class
audio = CoreAudio()
#audio = CoreAudio("audio_sweep.wav")

# Register your callback
audio.register(callback_function)

# Start audio processing
audio.start()

# Test reconfigure
audio.stop()
audio.configure(cutoff_freqs=[65, 73, 82, 87, 98, 110, 123, 131, 147, 165, 175, 196, 220, 247, 262, 294, 330, 349, 392, 440, 494, 523, 587, 659, 698, 784, 880, 988, 1046, 1175, 1319, 1397, 1568, 1760, 1975, 2093, 2349, 2637, 2794, 3136, 3520, 3951, 4186, 4699, 5274, 5588, 6272, 7040, 7902],
                trigger_offset=150000,
                trigger_threshold=150000)
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

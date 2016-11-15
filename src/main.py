# main file

import sys
sys.path.append('audio/src')
sys.path.append('backend/src')

from configuration import Configuration
from server import BackEnd
from core_audio import CoreAudio
import tone


backend = BackEnd()
audio = CoreAudio()

def onNewConfiguration(config):
    print("new saved config:")
    print(config)
    # audio.configure(...)
    # TODO: Translate the given notes to frequency bins + colors,
    # and set all configs to Audio. Use tone.NOTES to create the bins.

def onFrequencyDetected(freq):
    print(freq)
    # TODO
    # Start light

backend.register(onNewConfiguration)
backend.start()

audio.register(onFrequencyDetected)
# TODO set default config
audio.configure(cutoff_freqs=tone.getFrequenciesAsList(), output_binary=False)
#audio.configure(cutoff_freqs=[100, 500, 800, 1500, 3000], output_binary=False)
audio.start()


print("Pireworks started succesfully")

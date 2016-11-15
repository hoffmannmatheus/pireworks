# main file

import sys
sys.path.append('audio/src')
sys.path.append('backend/src')

from configuration import Configuration
from server import BackEnd
from core_audio import CoreAudio


backend = BackEnd()
audio = CoreAudio()
#light = Light?()

config = backend.getDefaultConfiguration()

def setConfigururation(c):
    audio.configure(
        cutoff_freqs=c.getCutoffFrequenciesAsList(),
        trigger_threshold=c.trigger_threshold,
        trigger_offset=c.trigger_offset,
        output_binary=False)

def onNewConfiguration(new_config):
    print("new saved config", new_config)
    setConfigururation(new_config)
    config = new_config

def onFrequencyDetected(frequencies):
    print(frequencies)
    # TODO
    # Use light + config
    # array of colors: config.getColorsForAllFrequencies()
    # light.display(...)

backend.register(onNewConfiguration)
backend.start()

audio.register(onFrequencyDetected)
#audio.configure(cutoff_freqs=[50, 500, 800, 1500, 3000], output_binary=False)
setConfigururation(config) # Sets the default config
audio.start()

print("Pireworks started succesfully")

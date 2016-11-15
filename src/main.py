# main file

import sys
import time

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
    print("new configuraiton being set...", c.toJson())
    audio.stop()
    time.sleep(3) # let it stop properly
    audio.configure(
        cutoff_freqs=c.getCutoffFrequenciesAsList(),
        trigger_threshold=c.trigger_threshold,
        trigger_offset=c.trigger_offset,
        output_binary=c.output_binary)
    audio.start()

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
setConfigururation(config)  # Sets the default config (see schema.sql)

print("Pireworks started succesfully")

audio.join()

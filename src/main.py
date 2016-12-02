# main file

import sys
import time

sys.path.append('audio/src')
sys.path.append('audio/test')
sys.path.append('backend/src')

from configuration import Configuration
from server import BackEnd
from core_audio import CoreAudio
from core_light import LightInput

backend = BackEnd()
audio = CoreAudio()
light = LightInput()

config = backend.getDefaultConfiguration()

def setConfigururation(c):
    print("new configuraiton being set...", c.toJson())
    audio.stop()
    time.sleep(3) # let it stop properly

    light.setColorSequence(c.getColorsForAllFrequencies())
    audio.configure(
        cutoff_freqs=c.getCutoffFrequenciesAsList(),
        trigger_threshold=c.trigger_threshold,
        trigger_offset=c.trigger_offset,
        output_binary=c.output_binary)
    audio.start()

def onNewConfiguration(new_config):
    setConfigururation(new_config)
    config = new_config

def onFrequencyDetected(frequencies):
    print(frequencies)
    light.colorMap(frequencies)


backend.register(onNewConfiguration)
backend.start()

audio.register(onFrequencyDetected)
setConfigururation(config)  # Sets the default config (see schema.sql)

light.startStrip()

print("Pireworks started succesfully")

audio.join()

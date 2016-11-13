# main file

import sys
sys.path.append('audio/src')
sys.path.append('backend/src')

from configuration import Configuration
from server import BackEnd
import tone

def my_callback(config):
    print("new saved config:")
    print(config)
    # TODO: Translate the given notes to frequency bins + colors,
    # and set all configs to Audio. Use tone.NOTES to create the bins.

backend = BackEnd()
backend.register(my_callback)
backend.start()

# TODO
# Start audio / light

print("Pireworks started succesfully")

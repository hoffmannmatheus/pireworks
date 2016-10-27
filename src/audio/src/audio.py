from core_audio import CoreAudio

# Define a function to take the list output
def callback_function(values):
    """My simple callback function"""
    print(values)

# This will create an audio instance to read from the microphone
a = CoreAudio()

# Register your callback
a.register(callback_function)

# Start the audio processing, this will spawn a thread for processing
a.start()

# In order to keep the audio thread running, this thread of execution cannot exit
# This call will block until audio exits
a.join()

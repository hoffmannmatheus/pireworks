# Audio Processor

## Overview

The audio processor is entirely controlled by the `CoreAudio` class.
See the comments in the code for a full description of the functions and variables, reference the following for a brief overview:

1. Create class instance
2. Register your callback function via the `register()` operation
3. (Optional) Configure your desired parameters via the `configure()` operation
4. Invoke the `start()` operation

*Note* If it is desired to re-configure the audio the following operations must be performed:

1. Invoke the `stop()` operation
2. Configure the desired paramters via the `configure()` operation
3. Invoke the `start()` operation

## RPi3 GPIO Usage

The `audio.py` module is configured as the main RPi3 entity. To execute simply call `python audio.py`

## General Usage

### Basic Operation

The following section describes basic operation using either the microphone input or file input
```python
from core_audio import CoreAudio

# Define a function to take the list output
def callback_function(values):
    """My simple callback function"""
    print(values)

# Use this constructor if you wish to read from the microphone
a = CoreAudio()

# Use this constructor if you wish to read from a file
a = CoreAudio("filename")

# Register your callback
a.register(callback_function)

# Start the audio processing, this will spawn a thread for processing
a.start()

# In order to keep the audio thread running, this thread of execution cannot exit
# This call will block until audio exits
a.join()
```

### Reconfiguration

The following section describes how to reconfigure audio, assuming the previous section has been implemented. See the table below for the configuration options.

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
|`cutoff_freqs`|list of int|20-22,000|A list of frequencies used to divide the frequeny spectrum|
|`trigger_threshold`|int|0-maxint|The magnitude required to trigger a signal|
|`trigger_offset`|int|0-maxint|The offset to apply to `trigger_threshold` to determine the maximum scaled output|
|`scaled_max_value`|int|0-maxint|The maximum scaled output value|
|`output_binary`|bool|True or False|Provide output to callback function in binary or scaled output|
|`rate`|int|44,000|The sample rate in Hertz|
|`chunk_size`|int|512 (or a multiple thereof)|Number of samples to process per loop|

As an example if the following code is used to configure the `CoreAudio`:

```python

# Processing must be stopped before reconfigure
a.stop()

# Reconfigure
a.configure(cutoff_freqs=[500,1000,1500,2000,2500],
            trigger_threshold=1000,
            trigger_offset=1000,
            scaled_max_value=255,
            output_binary=False)

# Restart processing
a.start()
```

Given the set of input shown in the figure below:

![Alt text](audio.png?raw=true "Audio Example")

The expected result would be as follows:

`[102, 255, 0, 0, 0]`

This is because the first frequency is above the `trigger_threshold` and 40% of `trigger_threshold` + `trigger_offset`. 
The second value is set to the `scaled_max_value` because it is larger than `trigger_threshold` + `trigger_offset`. 
The remaining values are zero because no signal was detected higher than the `trigger_threshold` in the respective bins. 

If the `output_binary` value was set to `True` then the following output would be observed:

 `[1, 1, 0, 0, 0]`

 Determination of the meaning of the output values is left as an excercise for the owner of the `callback_function`
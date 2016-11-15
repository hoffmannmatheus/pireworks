# Helpers to translate musical notes, colors and frequencies

import itertools

NOTES = {
    "C" : [262, 523, 1046, 2093, 4186],
    "D" : [294, 587, 1175, 2349, 4699],
    "E" : [330, 659, 1319, 2637, 5274],
    "F" : [349, 698, 1397, 2794, 5588],
    "G" : [392, 784, 1568, 3136, 6272],
    "A" : [440, 880, 1760, 3520, 7040],
    "B" : [494, 988, 1975, 3951, 7902]
}
DEFAULT_COLOR_MAP = {
    "C" : "FF0000",
    "D" : "FFFF00",
    "E" : "FF00FF",
    "F" : "FFFFFF",
    "G" : "00FFFF",
    "A" : "0000FF",
    "B" : "FF0FF0"
}

def toColorMap(color_list):
    """Translates a list of colors into a color map, in
    the proper order.
    Parameters
    ----------
    color_list : list
        The list of colors. Must have 7 colors, one for each note.
        The list must also be ordered as in NOTES.
    Returns
    ----------
    color_map : dict
        The notes to color map.
    """

    if type(color_list) is not list or len(color_list) != getNumberOfOctaves():
        # Must be a seven item list!
        return DEFAULT_COLOR_MAP
    return {
            "C" : color_list[0],
            "D" : color_list[1],
            "E" : color_list[2],
            "F" : color_list[3],
            "G" : color_list[4],
            "A" : color_list[5],
            "B" : color_list[6]
        }

def toColorList(color_map):
    """Translates a color map into a list of colors.
    Parameters
    ----------
    color_map : dict
        The notes to color map, similar to DEFAULT_COLOR_MAP.
    Returns
    ----------
    color_list : dict
        The list of colors being used, ordered by tone as DEFAULT_COLOR_MAP.
    """
    if not isValidColorMap(color_map):
        # Must be a seven item list!
        color_map = DEFAULT_COLOR_MAP
    return [
            color_map["C"],
            color_map["D"],
            color_map["E"],
            color_map["F"],
            color_map["G"],
            color_map["A"],
            color_map["B"]
        ]

def isValidColorMap(color_map):
    """Validates the given color_map.
    Parameters
    ----------
    color_map : dict
        The notes to color map, similar to DEFAULT_COLOR_MAP.
    Returns
    ----------
    is_valid : bool
        Is this a valid color map?
    """
    if type(color_map) is not list:
        return False  # Must be a list!
    if  len(color_map) != getNumberOfOctaves():
        return False  # Must have 7 items!
    if "C" not in color_map      \
        or "D" not in color_map  \
        or "E" not in color_map  \
        or "F" not in color_map  \
        or "G" not in color_map  \
        or "A" not in color_map  \
        or "B" not in color_map:
        return False  # Must have all 7 notes
    # Otherwise, its good
    return True

def getColorsForAllFrequencies(color_map):
    """Gets list of colors, given the colormap.
    Parameters
    ----------
    color_map : dict
        The notes to color map, similar to DEFAULT_COLOR_MAP.
    Returns
    ----------
    colors : list
        The complete list of colors for each tone, multiplied by the number of octaves.
    """
    return toColorList(color_map) * getNumberOfOctaves()


def getFrequenciesAsList():
    """Gets all frequencies.
    Returns
    ----------
    frequencies : list
        The complete list of frequencies, ascending order.
    """
    frequencies = list(itertools.chain.from_iterable(NOTES.values()))
    frequencies.sort()
    return frequencies

def getNumberOfOctaves():
    """Number of octaves available.
    Returns
    ----------
    octaves : number
        The number of octaves available for each note.
    """
    return len(NOTES["C"])

def getNumberOfNotes():
    """Number of notes available.
    Returns
    ----------
    notes : number
        The number of notes available.
    """
    return len(NOTES)
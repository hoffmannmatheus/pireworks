# Helpers to translate musical notes, colors and frequencies

import itertools

NOTES = {
    "C" : [252, 512, 1031, 2033, 4104],
    "D" : [274, 577, 1120, 2289, 4617],
    "E" : [320, 649, 1264, 2577, 5192],
    "F" : [339, 688, 1342, 2734, 5506],
    "G" : [382, 774, 1513, 3096, 6190],
    "A" : [430, 870, 1705, 3460, 6958],
    "B" : [484, 978, 1920, 3891, 7820]
}
DEFAULT_COLOR_MAP = {
    "C" : "red",
    "D" : "green",
    "E" : "blue",
    "F" : "teal",
    "G" : "purple",
    "A" : "aquamarine",
    "B" : "indigo"
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
    if type(color_map) is not dict:
        print("Not a dict!")
        return False  # Must be a list!
    if  len(color_map) != getNumberOfNotes():
        print("Invalid number of notes!")
        return False  # Must have 7 items!
    if "C" not in color_map      \
        or "D" not in color_map  \
        or "E" not in color_map  \
        or "F" not in color_map  \
        or "G" not in color_map  \
        or "A" not in color_map  \
        or "B" not in color_map:
        print("Should have A B C D E F G!")
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

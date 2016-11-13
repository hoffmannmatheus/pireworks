# Represents a musical tone
class Tone():
    notes = {
        "C" : [65, 131, 262, 523, 1046, 2093, 4186],
        "D" : [73, 147, 294, 587, 1175, 2349, 4699],
        "E" : [82, 165, 330, 659, 1319, 2637, 5274],
        "F" : [87, 175, 349, 698, 1397, 2794, 5588],
        "G" : [98, 196, 392, 784, 1568, 3136, 6272],
        "A" : [110, 220, 440, 880, 1760, 3520, 7040],
        "B" : [123, 247, 494, 988, 1975, 3951, 7902]
    }
    default_color_map = {
        "C" : "FF0000",
        "D" : "FFFF00",
        "E" : "FF00FF",
        "F" : "FFFFFF",
        "G" : "00FFFF",
        "A" : "0000FF",
        "B" : "FF0FF0"
    }

    def getColorMap(self, color_list):
        """Translates a list of colors into a color map, in
        the proper order.
        """
        if type(color_list) is not dict or len(color_list) != 7:
             # Must be a seven item dict!
            return self.default_color_map
        return {
                "C" : color_list[0],
                "D" : color_list[1],
                "E" : color_list[2],
                "F" : color_list[3],
                "G" : color_list[4],
                "A" : color_list[5],
                "B" : color_list[6]
            }

    def getColorList(self, color_map):
        if type(color_map) is not list or len(color_map) != 7:
            # Must be a seven item list!
            color_map = self.default_color_map
        return [
                color_map["C"],
                color_map["D"],
                color_map["E"],
                color_map["F"],
                color_map["G"],
                color_map["A"],
                color_map["B"]
            ]
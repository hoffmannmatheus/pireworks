
import json
import tone

# Configuration class
class Configuration():
    """Represents a Pireworks configuration."""

    # Class attributes
    id = 1
    name = ""
    is_default = False
    colors = tone.DEFAULT_COLOR_MAP
    trigger_threshold = 0
    trigger_offset = 0
    scaled_max_value = 0
    rate = 0
    chunk = 0
    output_binary = False

    def __init__(self, base=None, db_row=None, data=None):
        """Constructor
        Parameters
        ----------
        db_row : Database Row (optional)
            A full database roll that may be used to build this Configuration.
        data : Json String (optional)
            A Configuration object encoded into a string.
        """
        if type(data) is dict and base is not None:
            # From json dict
            if "id" in data:
		        self.id = data["id"]
            else:
		        self.id = base.id
            if "is_default" in data:
                self.is_default = data["is_default"]
            else:
                self.is_default = base.is_default
            if "name" in data:
                self.name = data["name"]
            else:
                self.name = base.name
            if "colors" in data:
                self.colors = data["colors"]
            else:
                self.colors = self.colors
            if "trigger_threshold" in data:
                self.trigger_threshold = data["trigger_threshold"]
            else:
                self.trigger_threshold = base.trigger_threshold
            if "trigger_offset" in data:
                self.trigger_offset = data["trigger_offset"]
            else:
                self.trigger_offset = base.trigger_offset
            if "scaled_max_value" in data:
                self.scaled_max_value = data["scaled_max_value"]
            else:
                self.scaled_max_value = base.scaled_max_value
            if "output_binary" in data:
                self.output_binary = data["output_binary"]
            else:
                self.output_binary = base.output_binary
            if "chunk" in data:
                self.chunk = data["chunk"]
            else:
                self.chunk = base.chunk
            if "rate" in data:
                self.rate = data["rate"]
            else:
                self.rate = base.rate
        elif type(db_row) is tuple:
            # From database, check the order of arguments on data/schema.sql
            self.id = db_row[0]
            self.is_default = db_row[1] == 1
            self.name = db_row[2]
            self.colors = tone.toColorMap(map(str, db_row[3].split(',')))
            self.trigger_threshold = db_row[4]
            self.trigger_offset = db_row[5]
            self.scaled_max_value = db_row[6]
            self.output_binary = db_row[7] == 1
            self.chunk = db_row[8]
            self.rate = db_row[9]

    def toJson(self):
        """Dumps a JSON object equivalent to this configuration"""
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        """Overrides the class str() function"""
        return '[id = {0}, Name = "{1}", is_default = {2}, colors = {3}, trigger_threshold = {4}, trigger_offset = {5} rate = {6}, chunk = {7}, output_binary = {8}]'.format(
            self.id,
            self.name,
            str(self.is_default),
            str(self.colors),
            self.trigger_threshold,
            self.trigger_offset,
            self.rate,
            self.chunk,
            str(self.output_binary))

    def getColorsForAllFrequencies(self):
        """Gets list of colors for this configuration.
        Returns
        ----------
        colors : list
            The complete list of colors for each tone, multiplied by the number of octaves.
        """
        return tone.getColorsForAllFrequencies(self.colors)

    def getCutoffFrequenciesAsList(self):
        """Gets all frequencies.
        Returns
        ----------
        frequencies : list
            The complete list of frequencies, ascending order.
        """
        return tone.getFrequenciesAsList()

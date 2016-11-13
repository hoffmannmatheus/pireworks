
from tone import Tone

# Configuration class
class Configuration():
    """Represents a Pireworks configuration."""

    # Class attributes
    id = 1
    name = ""
    is_default = False
    colors = Tone().default_color_map
    trigger_threshold = 0
    trigger_offset = 0
    scaled_max_value = 0
    rate = 0
    chunk = 0
    output_binary = False

    def __init__(self, db_row=None):
        """Consturctor
        Parameters
        ----------
        db_row : Database Row (optional)
            A full database roll that may be used to build this Configuration.
        """
        if type(db_row) is tuple:
            # Check the order of arguments on data/schema.sql
            self.id = db_row[0]
            self.is_default = db_row[1] == 1
            self.name = db_row[2]
            color_list = map(str, db_row[3].split(','))
            self.colors = Tone().getColorMap(color_list)
            self.trigger_threshold = db_row[4]
            self.trigger_offset = db_row[5]
            self.scaled_max_value = db_row[6]
            self.output_binary = db_row[7] == 1
            self.chunk = db_row[8]
            self.rate = db_row[9]

    def __str__(self):
        """Overrides the class str() function"""
        return '[id = {0}, Name = "{1}", is_default = {2}, colors = {3}, trigger_threshold = {4}, rate = {5}, chunk = {6}, output_binary = {7}]'.format(
                        self.id,
                        self.name,
                        str(self.is_default),
                        str(self.colors),
                        self.trigger_threshold,
                        self.rate,
                        self.chunk,
                        str(self.output_binary)); 
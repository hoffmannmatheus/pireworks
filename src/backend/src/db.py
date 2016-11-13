"""Provides a SQLite database abstraction."""

import sqlite3
import tone
from configuration import Configuration

# Default paths and values
DB_PATH = 'backend/src/data/db.sqlite'
SCHEMA_PATH = 'backend/src/data/schema.sql'

# Queries
QUERY_INSERT_CONFIG = 'INSERT INTO \
    configuration ( \
        is_default, name, colors, trigger_threshold, trigger_offset, scaled_max_value, \
        output_binary, chunk, rate ) \
    VALUES ( \
        {is_default}, "{name}", "{colors}", {trigger_threshold}, {trigger_offset}, {scaled_max_value}, \
        {output_binary}, {chunk}, {rate} );'

QUERY_UPDATE_CONFIG = 'REPLACE INTO \
    configuration ( \
        id, \
        is_default, name, colors, trigger_threshold, trigger_offset, scaled_max_value, \
        output_binary, chunk, rate ) \
    VALUES ( \
        {id}, \
        {is_default}, "{name}", "{colors}", {trigger_threshold}, {trigger_offset}, {scaled_max_value}, \
        {output_binary}, {chunk}, {rate} );'

QUERY_SELECT_DEFAULT = 'SELECT * FROM configuration WHERE is_default = 1 LIMIT 1;'

QUERY_SELECT_ALL = 'SELECT * FROM configuration ORDER BY id DESC;'

def setup():
    """Sets up the database.
     
     This method should be called at every time the system starts up,
     as it will create the database in case it does not exist yet.
     
     See data/schema.sql for details on how the database is structured.
     """
    schema = open(SCHEMA_PATH, 'r').read()
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()
    cursor.executescript(schema)
    connection.commit()

    cursor.close()
    connection.close()

def getDefaultConfiguration():
    """Returns the default configuration.
    Returns
    ----------
    configuration: Configuration
        The default configuration."""
    configuration = None 
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Run it
    try:
        cursor.execute(QUERY_SELECT_DEFAULT)
        for row in cursor.fetchall():
            configuration = Configuration(db_row=row)
    except sqlite3.IntegrityError as e:
        print('(getDefaultConfiguration) Error: ' + str(e))

    # Free cursors
    cursor.close()
    connection.close()

    return configuration

def getConfigurations():
    """Returns the list of saved configurations.
    Returns
    ----------
    configurations: [Configuration]
        All configurations stored in the database."""
    configurations = []

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Run it
    try:
        cursor.execute(QUERY_SELECT_ALL)
        for row in cursor.fetchall():
            configurations.append(Configuration(db_row=row))
    except sqlite3.IntegrityError as e:
        print('(getConfigurations) Error: ' + str(e))

    # Free cursors
    cursor.close()
    connection.close()

    return configurations

def saveConfiguration(config, update=False):
    """Saves the given configuration to the database.
   
    Parameters
    ----------
    config : Configuration
        The Configuration to be saved.
    update : bool
        Set this to True to update an existant configuration in the DB (must have an ID).
        Default is False, which means it will simply insert a new configuraiton.
    
    Returns
    ----------
    success : bool
        Was the configuration saved?
    """
    success = False
    if not isinstance(config, Configuration):
        return success
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Setup query
    query = QUERY_UPDATE_CONFIG if update else QUERY_INSERT_CONFIG
    query = query.format(
        id = config.id,
        is_default= 1 if config.is_default else 0,
        name=config.name, 
        colors=','.join(tone.toColorList(config.colors)),
        trigger_threshold=config.trigger_threshold,
        trigger_offset=config.trigger_offset,
        scaled_max_value=config.scaled_max_value,
        output_binary= 1 if config.output_binary else 0,
        chunk=config.chunk,
        rate=config.rate)
        
    # Run it
    try:
        cursor.execute(query)
        connection.commit()
        success = True
    except sqlite3.IntegrityError as e:
        print('(saveConfiguration) Error: ' + str(e))

    # Free cursors
    cursor.close()
    connection.close()
    
    return success
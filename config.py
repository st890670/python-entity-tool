# initial config file
from configparser import ConfigParser


def db_config(filename='config.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in {} file'.format(section, filename))

    return db


def output_config(filename='config.ini', section='output'):
    parser = ConfigParser()
    parser.read(filename)
    return parser[section]

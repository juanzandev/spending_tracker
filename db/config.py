import os
from configparser import ConfigParser


def config(filename="db/database.ini", section="postgresql"):
    parser = ConfigParser()
    with open(filename, 'r', encoding='utf-8') as file:
        parser.read_file(file)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            print(f"{param[0]}: {param[1]}")
            db[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file.")

    return db

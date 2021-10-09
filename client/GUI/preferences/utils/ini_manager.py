import configparser


def get_ini(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    sections_dict = {}

    # Get all defaults
    defaults = config.defaults()
    temp_dict = {}
    for key in defaults:
        temp_dict[key] = defaults[key]

    sections_dict['default'] = temp_dict

    # Get sections and iterate over each
    sections = config.sections()

    for section in sections:
        options = config.options(section)
        temp_dict = {}
        for option in options:
            temp_dict[option] = config.get(section, option)

        sections_dict[section] = temp_dict

    return sections_dict


def set_ini(file_path, section, setting, value):
    # Load the current preferences into the config parser
    config = configparser.ConfigParser()
    current_preferences = get_ini(file_path)
    for temp_section in current_preferences:
        config[temp_section] = current_preferences[temp_section]

    # Change the requested setting
    config[section][setting] = value

    # Write the changes to file
    with open(file_path, 'w') as configfile:
        config.write(configfile)

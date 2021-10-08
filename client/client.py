import sys
import configparser

from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMenuBar, QGridLayout, QWidget, QLineEdit, QPushButton
import zmq

PREFERENCES_PATH = "client/preferences.ini"


def get_preferences():
    config = configparser.ConfigParser()
    config.read(PREFERENCES_PATH)

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


def set_preferences(section, setting, value):
    # Load the current preferences into the config parser
    config = configparser.ConfigParser()
    current_preferences = get_preferences()
    for temp_section in current_preferences:
        config[temp_section] = current_preferences[temp_section]

    # Change the requested setting
    config[section][setting] = value

    # Write the changes to file
    with open(PREFERENCES_PATH, 'w') as configfile:
        config.write(configfile)


class Preferences(QMainWindow):
    """Preferences window."""

    settings_indexes = {}
    feedback_label = None
    preferences = None

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Speil - Preferences")
        wid = QWidget(self)
        self.setCentralWidget(wid)
        grid = QGridLayout()
        wid.setLayout(grid)
        save_button = QPushButton("Save")
        grid.addWidget(save_button, 0, 0)
        save_button.clicked.connect(self.save_values)
        reload_button = QPushButton("Reload preferences")
        grid.addWidget(reload_button, 0, 1)
        reload_button.clicked.connect(self.load_values)
        self.feedback_label = QLabel()
        grid.addWidget(self.feedback_label, 0, 2)

        self.preferences = get_preferences()

        highest_x_coordinate = 0
        highest_y_coordinate = 0
        for section_index in range(len(self.preferences.keys())):
            highest_x_coordinate += 2

            section_name = list(self.preferences.keys())[section_index]
            grid.addWidget(QLabel(section_name.upper() + ":"), 1, section_index * 2)

            for setting_index in range(len(self.preferences[section_name].keys())):
                highest_y_coordinate += 1

                setting_name = list(self.preferences[section_name].keys())[setting_index]
                grid.addWidget(QLabel(setting_name), setting_index + 2, section_index * 2)

                value_line = QLineEdit()
                grid.addWidget(value_line, setting_index + 2, section_index * 2 + 1)
                self.settings_indexes[setting_name] = grid.indexOf(value_line)

        self.load_values()

    def load_values(self):
        self.preferences = get_preferences()

        for section in self.preferences:
            for setting in self.preferences[section]:
                grid_id = self.settings_indexes[setting]
                self.centralWidget().layout().itemAt(grid_id).widget().setText(self.preferences[section][setting])

        self.feedback_label.setText("Loaded settings successfully...")

    def save_values(self):
        preferences = get_preferences()
        for section in preferences:
            for setting in preferences[section]:
                grid_id = self.settings_indexes[setting]
                new_value = self.centralWidget().layout().itemAt(grid_id).widget().text()
                set_preferences(section, setting, new_value)

        self.feedback_label.setText("Settings saved successfully...   ")
        self.load_values()


class MainWindow(QMainWindow):
    """Main Window."""

    zmq_context = None
    socket = None
    preferences = None

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.initialize_networking()
        self.preferences = Preferences(self)
        self.setWindowTitle("Speil")
        self.resize(640, 480)
        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        preferences = menu_bar.addAction("Preferences")
        preferences.triggered.connect(lambda: self.preferences.show())

    def _initialize_networking(self):
        self.zmq_context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        server_address = "tcp://" +\
                         self.preferences.preferences["authentication"]["server_address"] +\
                         ":" +\
                         self.preferences.preferences["authentication"]["server_port"]
        self.socket.connect(server_address)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

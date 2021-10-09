from PyQt5.QtWidgets import QLabel, QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton
from ..preferences.utils import ini_manager


class Preferences(QMainWindow):
    """Preferences window."""

    preferences_path = ""

    settings_indexes = {}
    feedback_label = None
    preferences = None

    def __init__(self, preferences_path, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.preferences_path = preferences_path
        self.setWindowTitle("Speil - Preferences")
        preferences_widget = QWidget(self)
        self.setCentralWidget(preferences_widget)
        grid = QGridLayout()
        preferences_widget.setLayout(grid)
        save_button = QPushButton("Save")
        grid.addWidget(save_button, 0, 0)
        save_button.clicked.connect(self.save_values)
        reload_button = QPushButton("Reload preferences")
        grid.addWidget(reload_button, 0, 1)
        reload_button.clicked.connect(self.load_values)
        self.feedback_label = QLabel()
        grid.addWidget(self.feedback_label, 0, 2)
        self.preferences = ini_manager.get_ini(self.preferences_path)

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
        self.preferences = ini_manager.get_ini(self.preferences_path)

        for section in self.preferences:
            for setting in self.preferences[section]:
                grid_id = self.settings_indexes[setting]
                self.centralWidget().layout().itemAt(grid_id).widget().setText(self.preferences[section][setting])

        self.feedback_label.setText("Loaded settings successfully...")

    def save_values(self):
        preferences = ini_manager.get_ini(self.preferences_path)
        for section in preferences:
            for setting in preferences[section]:
                grid_id = self.settings_indexes[setting]
                new_value = self.centralWidget().layout().itemAt(grid_id).widget().text()
                ini_manager.set_ini(self.preferences_path, section, setting, new_value)

        self.feedback_label.setText("Settings saved successfully...   ")
        self.load_values()

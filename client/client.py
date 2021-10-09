# Public packages
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
import zmq

# Private packages
from networking import authentication
from GUI.preferences import preferences_window
from GUI import menu_bar, login_page

PREFERENCES_PATH = "client/preferences.ini"


class MainWindow(QMainWindow):
    """Main Window."""

    # Networking
    zmq_context = None
    socket = None
    connection_id = None

    # Sub-windows
    preferences = None

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Speil")

        # Initialize networking
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(zmq.REQ)

        # Center this window on screen
        qt_rectangle = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rectangle.moveCenter(center_point)
        self.move(qt_rectangle.topLeft())

        # Populate GUI with content and sub-windows
        self.preferences = preferences_window.Preferences(PREFERENCES_PATH, self)
        menu_bar.create_menu_bar(self)
        login_page.create_login_page(self)

    # Belongs in 'networking' package you say? Yuh, but python pathing fucked me in the arse so no.
    def login(self, server_address, server_password):
        login_attempt = authentication.connect_to_server(self, server_address, server_password)
        print(login_attempt)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

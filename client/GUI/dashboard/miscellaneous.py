from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class Miscellaneous(QWidget):
    dashboard_window = None
    vbox = None
    reload_button = None

    def __init__(self, parent):
        QWidget.__init__(self)
        self.dashboard_window = parent
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)
        self.reload_button = QPushButton("Reload client list")
        self.vbox.addWidget(self.reload_button)
        self.reload_button.clicked.connect(self._reload_button_clicked)

    def _reload_button_clicked(self):
        self.dashboard_window.available_client_view.load_client_information()

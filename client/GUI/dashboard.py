from PyQt5.QtWidgets import QWidget, QHBoxLayout, QGridLayout, QLabel


class Dashboard(QWidget):
    available_client_view = None
    temp = None

    def __init__(self, parent):
        QWidget.__init__(self)
        self.setLayout(QHBoxLayout())
        self.available_client_view = AvailableClientView(self)
        self.layout().addWidget(self.available_client_view)
        self.temp = QLabel("Temp")
        self.layout().addWidget(self.temp)


class AvailableClientView(QWidget):
    grid = None

    def __init__(self, parent):
        QWidget.__init__(self)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

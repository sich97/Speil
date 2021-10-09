from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ..dashboard import client_view, miscellaneous


class Dashboard(QWidget):
    main_window = None
    available_client_view = None
    miscellaneous = None

    def __init__(self, parent):
        QWidget.__init__(self)
        self.main_window = parent
        self.setLayout(QHBoxLayout())
        self.available_client_view = client_view.AvailableClientView(self)
        self.layout().addWidget(self.available_client_view)
        self.miscellaneous = miscellaneous.Miscellaneous(self)
        self.layout().addWidget(self.miscellaneous)

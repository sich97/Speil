from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel


class ClientListItem(QWidget):
    h_box = None
    connection_id = None
    name = None
    is_streaming = None

    def __init__(self, connection_id, name, is_streaming, parent=None):
        super(ClientListItem, self).__init__(parent)
        self.h_box = QHBoxLayout()
        self.setLayout(self.h_box)
        self.connection_id = connection_id
        self.name = name
        self.is_streaming = is_streaming

        self.h_box.addWidget(QLabel(connection_id))
        self.h_box.addWidget(QLabel(name))
        self.h_box.addWidget(QLabel(str(is_streaming)))

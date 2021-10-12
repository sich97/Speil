from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel


class StreamWindow(QMainWindow):
    client_item = None

    def __init__(self, client_item, parent=None):
        super().__init__(parent)
        self.client_item = client_item
        self.setWindowTitle("Speil - Streamer")
        stream_window_widget = QWidget(self)
        self.setCentralWidget(stream_window_widget)
        v_box = QVBoxLayout()
        stream_window_widget.setLayout(v_box)
        v_box.addWidget(QLabel("Test"))

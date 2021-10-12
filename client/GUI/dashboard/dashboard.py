from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ..dashboard import client_view, miscellaneous
from ..stream_window import stream_window


class Dashboard(QWidget):
    main_window = None
    available_client_view = None
    miscellaneous = None

    stream_windows = []

    def __init__(self, parent):
        QWidget.__init__(self)
        self.main_window = parent
        self.setLayout(QHBoxLayout())
        self.available_client_view = client_view.AvailableClientView(self)
        self.layout().addWidget(self.available_client_view)
        self.miscellaneous = miscellaneous.Miscellaneous(self)
        self.layout().addWidget(self.miscellaneous)

    def client_item_double_clicked(self, q_model_index):
        client_item = self.available_client_view.itemWidget(
            self.available_client_view.itemFromIndex(q_model_index))

        if not client_item.is_streaming:
            reply_status, reply_data = self.main_window.start_remote_stream(client_item.connection_id)
            if not reply_status == 1:
                print(reply_data)

        self.stream_windows.append(stream_window.StreamWindow(self, client_item))
        self.stream_windows[-1].show()

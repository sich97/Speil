from PyQt5.QtWidgets import QListWidget, QWidget, QHBoxLayout, QLabel, QListWidgetItem

from ..dashboard import client_item


class AvailableClientView(QListWidget):
    dashboard_window = None

    def __init__(self, parent):
        QListWidget.__init__(self)
        self.dashboard_window = parent
        self.load_client_information()
        self.doubleClicked.connect(self.dashboard_window.client_item_double_clicked)

    def load_client_information(self):
        # Clear the layout
        for i in reversed(range(self.count())):
            self.takeItem(i)

        # Create the header
        header = QWidget()
        header_layout = QHBoxLayout()
        header.setLayout(header_layout)
        header_layout.addWidget(QLabel("Connection ID"))
        header_layout.addWidget(QLabel("Name"))
        header_layout.addWidget(QLabel("Is streaming"))
        self.add_widget_to_list(header)

        # Fill the list with available clients
        available_client_information = self.dashboard_window.main_window.get_available_clients()
        for connection_id in available_client_information:
            client_name = available_client_information[connection_id][0]
            client_is_streaming = available_client_information[connection_id][1]
            self.add_widget_to_list(client_item.ClientListItem(connection_id, client_name, client_is_streaming))

        # Adjust viewport size to fit list
        minimum_width = int(self.sizeHintForColumn(0) * 1.5)
        self.setMinimumWidth(minimum_width)
        self.setMinimumHeight(minimum_width)

    def add_widget_to_list(self, widget):
        q_list_widget_item = QListWidgetItem(self)
        q_list_widget_item.setSizeHint(widget.sizeHint())
        self.addItem(q_list_widget_item)
        widget.show()
        self.setItemWidget(q_list_widget_item, widget)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


def create_login_page(parent):
    login_widget = QWidget()
    parent.window_login_page = login_widget
    v_split = QVBoxLayout()
    login_widget.setLayout(v_split)
    parent.setCentralWidget(login_widget)
    v_split.setContentsMargins(10, 25, 10, 30)

    text_label1 = QLabel("Welcome to Speil!")
    v_split.addWidget(text_label1)
    text_label2 = QLabel("Login to your self-hosted server below:")
    text_label2.setContentsMargins(0, 0, 0, 10)
    v_split.addWidget(text_label2)

    default_server_address = parent.window_preferences.preferences["authentication"]["server_address"]\
        + ":" + parent.window_preferences.preferences["authentication"]["server_port"]
    server_address_box = QLineEdit(default_server_address)
    server_address_box.setPlaceholderText("0.0.0.0:1234")
    v_split.addWidget(server_address_box)

    password_box = QLineEdit()
    password_box.setPlaceholderText("Password...")
    v_split.addWidget(password_box)

    login_button = QPushButton("Login")
    v_split.addWidget(login_button)
    login_button.clicked.connect(lambda: parent.login(server_address_box.text(), password_box.text()))

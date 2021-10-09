from PyQt5.QtWidgets import QMenuBar


def create_menu_bar(parent):
    menu_bar = QMenuBar(parent)
    parent.setMenuBar(menu_bar)
    preferences = menu_bar.addAction("Preferences")
    preferences.triggered.connect(lambda: parent.preferences.show())

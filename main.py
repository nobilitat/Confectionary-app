import sys
from PySide6 import QtWidgets, QtGui
from ConnectToDatabase import ConnectToDatabase
from MainWindow import MainWindow


def confectionary():
    app = QtWidgets.QApplication([])

    widget = MainWindow()
    widget.show()
    login, password = widget.connect_dialog()

    connect_object = ConnectToDatabase(login, password)
    connect = connect_object.connect_db()
    widget.connect = connect
    widget.open_supply_widget()

    if connect:
        print("Подключение установлено")

    sys.exit(app.exec())


if __name__ == '__main__':
    confectionary()

from PySide6 import QtCore, QtWidgets, QtGui

class AddSupplyWindow(QtWidgets.QWidget):
    """Окно добавления поставки"""

    def __init__(self, connect):
        super(AddSupplyWindow, self).__init__()

        self.resize(350, 130)
        self.setWindowTitle('Добавление новой поставки')
        self.connect = connect

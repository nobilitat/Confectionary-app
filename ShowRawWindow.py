from PySide6 import QtCore, QtWidgets, QtGui
from AddRawWindow import AddRawWindow
from AdditionalFunctions import get_units


class ShowRawWindow(QtWidgets.QWidget):
    """Окно просмотра, добавления сырья"""

    def __init__(self, connect):
        super(ShowRawWindow, self).__init__()

        self.resize(550, 400)
        self.setWindowTitle('Просмотр сырья')
        self.connect = connect

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_new_raw)
        self.update_button = QtWidgets.QPushButton('Обновить')
        self.update_button.clicked.connect(self.update_getting_raw)

        self.model = QtGui.QStandardItemModel()
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.table.verticalHeader().hide()

        self.model.setHorizontalHeaderItem(0, QtGui.QStandardItem('ID'))
        self.model.setHorizontalHeaderItem(1, QtGui.QStandardItem('Наименование'))
        self.model.setHorizontalHeaderItem(2, QtGui.QStandardItem('Остаток'))
        self.model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Ед. изм.'))

        self.table.setColumnWidth(0, 70)
        self.table.setColumnWidth(1, 215)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 110)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.h_layout.addWidget(self.add_button)
        self.h_layout.addWidget(self.update_button)

        self.layout.addLayout(self.h_layout)

        self.layout.addWidget(self.table)

    @QtCore.Slot()
    def update_getting_raw(self):
        result = self.get_raw()

        self.model.setRowCount(0)

        for i in result[::-1]:
            self.model.insertRow(
                0,
                [
                    QtGui.QStandardItem(str(i[0])),
                    QtGui.QStandardItem(i[1]),
                    QtGui.QStandardItem(str(i[2])),
                    QtGui.QStandardItem(str(i[3]))
                 ]
            )

    @QtCore.Slot()
    def add_new_raw(self):
        """Вызов окна добавления сырья"""

        self.add_raw = AddRawWindow(self.connect)
        units = get_units(self.connect)
        for i in units:
            self.add_raw.unit.addItems(i)

        self.add_raw.show()

    def get_raw(self):
        if self.connect:
            cursor = self.connect.cursor()

            request = """
            select
                r.raw_id,
                r.raw_name,
                r.raw_reserve,
                (select u.unit_name from unit u where u.unit_id = r.unit_id)
            from
                raw r
           """

            cursor.execute(request)
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            print('Нет соедниния с базой данных')

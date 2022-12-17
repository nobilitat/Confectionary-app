from PySide6 import QtCore, QtWidgets, QtGui
from AddSupplierWindow import AddSupplierWindow

class ShowSupplierWindow(QtWidgets.QWidget):
    """Окно просмотра, добавления поставщиков"""

    def __init__(self, connect):
        super(ShowSupplierWindow, self).__init__()

        self.resize(660, 400)
        self.setWindowTitle('Окно просмотра поставщиков')
        self.connect = connect

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.add_button.clicked.connect(self.add_new_supplier)
        self.update_button = QtWidgets.QPushButton('Обновить')
        self.update_button.clicked.connect(self.update_getting_supplier)

        self.model = QtGui.QStandardItemModel()
        self.table = QtWidgets.QTableView()
        self.table.setModel(self.model)
        self.table.verticalHeader().hide()

        self.model.setHorizontalHeaderItem(0, QtGui.QStandardItem('ID'))
        self.model.setHorizontalHeaderItem(1, QtGui.QStandardItem('Наименование'))
        self.model.setHorizontalHeaderItem(2, QtGui.QStandardItem('Адрес'))
        self.model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Телефон'))

        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 215)
        self.table.setColumnWidth(2, 245)
        self.table.setColumnWidth(3, 130)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.h_layout = QtWidgets.QHBoxLayout(self)
        self.h_layout.addWidget(self.add_button)
        self.h_layout.addWidget(self.update_button)

        self.layout.addLayout(self.h_layout)
        self.layout.addWidget(self.table)

    @QtCore.Slot()
    def update_getting_supplier(self):
        result = self.get_supplier()

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
    def add_new_supplier(self):
        """Вызов окна добавления сырья"""

        self.add_supplier = AddSupplierWindow(self.connect)

        self.add_supplier.show()

    def get_supplier(self):
        if self.connect:
            cursor = self.connect.cursor()

            request = """
            select 
                s.supplier_id,
                s.supplier_name,
                s.supplier_address,
                s.supplier_phone
            from supplier s 
           """

            cursor.execute(request)
            result = cursor.fetchall()
            cursor.close()
            return result
        else:
            print('Нет соедниния с базой данных')

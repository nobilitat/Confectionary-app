from PySide6 import QtWidgets, QtCore


class AddSupplierWindow(QtWidgets.QWidget):
    """Окно добавления поставщика"""

    def __init__(self, connect):
        super(AddSupplierWindow, self).__init__()

        self.resize(350, 130)
        self.setWindowTitle('Добавление нового поставщика')
        self.connect = connect

        self.validation_field = QtWidgets.QLabel()
        self.validation_field.setStyleSheet("color: red;")

        self.title = QtWidgets.QLabel('Добавление нового поставщика')
        self.name = QtWidgets.QLineEdit()
        self.name.setStyleSheet('QLineEdit::hover { border: none }')
        self.name.setPlaceholderText('Наименование')
        self.address = QtWidgets.QLineEdit()
        self.address.setStyleSheet('QLineEdit::hover { border: none }')
        self.address.setPlaceholderText('Адрес')
        self.phone = QtWidgets.QLineEdit()
        self.phone.setStyleSheet('QLineEdit::hover { border: none }')
        self.phone.setPlaceholderText('Номер телефона')
        self.button = QtWidgets.QPushButton('Добавить')
        self.button.clicked.connect(self.add_supplier)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.validation_field)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.address)
        self.layout.addWidget(self.phone)
        self.layout.addWidget(self.button)

    @QtCore.Slot()
    def add_supplier(self):
        name = self.name.text()
        phone = self.phone.text()
        address = self.address.text()

        if not name or not phone or not address:
            self.validation_field.setText('Не все поля заполнены')
            return

        request = f"""
            insert into supplier
            (supplier_name, supplier_address, supplier_phone)
            values
            ('{name}', '{address}', '{phone}')
        """

        if self.connect:
            cursor = self.connect.cursor()
            cursor.execute(request)
            self.connect.commit()
            cursor.close()
            self.close()
        else:
            print('Нет соедниния с базой данных')

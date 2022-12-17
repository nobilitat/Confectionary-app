from PySide6 import QtWidgets, QtCore


class AddRawWindow(QtWidgets.QWidget):
    """Окно добавления сырья"""

    def __init__(self, connect):
        super(AddRawWindow, self).__init__()

        self.resize(350, 130)
        self.setWindowTitle('Добавление нового сырья')
        self.connect = connect

        self.validation_field = QtWidgets.QLabel()
        self.validation_field.setStyleSheet("color: red;")

        self.title = QtWidgets.QLabel('Добавление нового сырья')
        self.name = QtWidgets.QLineEdit()
        self.name.setStyleSheet('QLineEdit::hover { border: none }')
        self.name.setPlaceholderText('Наименование сырья')
        self.reserve = QtWidgets.QLineEdit()
        self.reserve.setStyleSheet('QLineEdit::hover { border: none }')
        self.reserve.setPlaceholderText('Количество на остатке')

        self.unit = QtWidgets.QComboBox()
        self.unit.setPlaceholderText('Выберите единицу измерения')

        self.button = QtWidgets.QPushButton('Добавить')
        self.button.clicked.connect(self.add_raw)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.validation_field)
        self.layout.addWidget(self.name)
        self.layout.addWidget(self.reserve)
        self.layout.addWidget(self.unit)
        self.layout.addWidget(self.button)

    def add_raw(self):
        name = self.name.text()
        reserve = self.reserve.text()
        unit = self.unit.currentText()

        if not name or not reserve or not unit:
            self.validation_field.setText('Не все поля заполнены')
            return

        if self.connect:
            cursor = self.connect.cursor()

            request = f"""
                insert into raw
                (raw_name, raw_reserve, unit_id)
                values
                ('{name}', 
                '{reserve}', 
                (select unit_id from unit where unit_name = '{unit}'))
            """

            cursor.execute(request)
            self.connect.commit()
            cursor.close()
            self.close()
        else:
            print('Нет соедниния с базой данных')

from PySide6 import QtCore, QtWidgets, QtGui
from ConnectToDatabase import ConnectToDatabase


class ConnectDialogWindow(QtWidgets.QDialog):
    """Диалоговое окно для подключения к базе данных"""

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('icon-cake.png'))

        self.resize(450, 110)
        self.setWindowTitle('Подключение к базе данных')

        self.login_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.login_input.setPlaceholderText('Логин')
        self.login_input.setStyleSheet('QLineEdit::hover { border: none }')
        self.password_input.setPlaceholderText('Пароль')
        self.password_input.setStyleSheet('QLineEdit::hover { border: none }')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.error_label = QtWidgets.QLabel()
        self.error_label.setStyleSheet("color: red;")
        # self.error_label.hide()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.error_label)
        self.layout.addWidget(self.login_input)
        self.layout.addWidget(self.password_input)

        self.ok_button = QtWidgets.QPushButton("Подключиться")
        self.cancel_button = QtWidgets.QPushButton("Отмена")

        self.button_layout = QtWidgets.QHBoxLayout(self)
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.ok_button.clicked.connect(self.connect_to_db)
        self.cancel_button.clicked.connect(QtCore.QCoreApplication.quit())

    def closeEvent(self, event):
        """Переопределение метода события вызываемого при закрытии окна"""
        if event.spontaneous():
            msg_box = QtWidgets.QMessageBox()
            msg_box.setFont(QtGui.QFont('times', 10))
            msg_box.setWindowTitle('Выход из программы')
            msg_box.setText('Вы уверены, что хотите выйти из программы?')
            msg_box.addButton('Да', QtWidgets.QMessageBox.ButtonRole.YesRole)
            msg_box.addButton('Нет', QtWidgets.QMessageBox.ButtonRole.NoRole)
            result = msg_box.exec()

            self.close() if not result else event.ignore()

    @QtCore.Slot()
    def close_app(self):
        print('close')
        self.close()

    @QtCore.Slot()
    def connect_to_db(self):
        LOGIN = self.login_input.text()
        PASSWORD = self.password_input.text()
        self.error_label.setText('Ошибка подключения: неверный логин или пароль')

        connect = ConnectToDatabase(LOGIN, PASSWORD)
        connect.connect_db()

        if connect:
            connect.close()
            self.close()
            return True

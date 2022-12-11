from PySide6 import QtCore, QtWidgets, QtGui
from ConnectDialogWindow import ConnectDialogWindow
from AddSupplierWindow import AddSupplierWindow
from ShowRawWindow import ShowRawWindow


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('image/icon-cake.png'))

        self.dialog = None
        self.connect = None

        self.resize(900, 600)
        self.setWindowTitle('Кондитерское производство')

        self.font = QtGui.QFont('times', 10)

        # Describe menu actions
        new_supply = QtGui.QAction('Новая поставка', self)
        show_supplies = QtGui.QAction('Просмотр поставок', self)
        show_raws = QtGui.QAction('Сырье', self)
        show_raws.triggered.connect(self.option_raws)
        new_supplier = QtGui.QAction('Новый поставщик', self)
        new_supplier.triggered.connect(self.add_new_supplier)
        show_supplier = QtGui.QAction('Просмотр поставщиков', self)
        new_production = QtGui.QAction('Новый выпуск', self)
        show_productions = QtGui.QAction('Просмотр выпусков', self)
        new_product = QtGui.QAction('Новый продукт', self)
        show_product = QtGui.QAction('Просмотр продуктов', self)
        new_order = QtGui.QAction('Новый заказ', self)
        show_order = QtGui.QAction('Просмотр заказов', self)

        # create menuBar and add actions to menu
        menu = self.menuBar()
        menu.setFont(self.font)
        menu_supply = menu.addMenu('Поставка сырья')
        menu_supply.setFont(self.font)
        menu_supply.addAction(new_supply)
        menu_supply.addAction(show_supplies)
        menu_supply.addAction(show_raws)
        menu_supply.addAction(new_supplier)
        menu_supply.addAction(show_supplier)
        menu_production = menu.addMenu('Производство')
        menu_production.setFont(self.font)
        menu_production.addAction(new_production)
        menu_production.addAction(show_productions)
        menu_production.addAction(new_product)
        menu_production.addAction(show_product)
        menu_order = menu.addMenu('Заказы')
        menu_order.setFont(self.font)
        menu_order.addAction(new_order)
        menu_order.addAction(show_order)

        self.title = QtWidgets.QLabel()

        # widget for table
        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)

        # model for table
        self.model = QtGui.QStandardItemModel()

        # Table show
        self.main_layout = QtWidgets.QVBoxLayout(self.widget)

        self.main_table = QtWidgets.QTableView()
        self.main_table.setModel(self.model)

        self.main_layout.addWidget(self.title)
        self.main_layout.addWidget(self.main_table)

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

            self.dialog.close() if not result else event.ignore()

    def connect_dialog(self):
        """Вызов диалогового окна для подключения к БД"""
        self.dialog = ConnectDialogWindow()
        self.dialog.show()
        self.dialog.exec()

        return self.dialog.login_input.text(), self.dialog.password_input.text()

    @QtCore.Slot()
    def add_new_supplier(self):
        """Вызов окна добавления поставщика"""

        self.add_supplier = AddSupplierWindow(self.connect)
        self.add_supplier.show()

    @QtCore.Slot()
    def option_raws(self):
        """Вызов окна просмотра всего сырья"""

        self.show_raws = ShowRawWindow(self.connect)
        self.show_raws.show()
        self.show_raws.update_getting_raw()

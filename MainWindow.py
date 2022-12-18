from PySide6 import QtCore, QtWidgets, QtGui
from ConnectDialogWindow import ConnectDialogWindow
from ShowSupplierWindow import ShowSupplierWindow
from ShowRawWindow import ShowRawWindow


class MainWindow(QtWidgets.QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('image/icon-cake.png'))

        self.dialog = None
        self.connect = None
        self.close_button = None
        self.update_button = None
        self.new_button = None

        self.showMaximized()
        self.setWindowTitle('Кондитерское производство')

        self.font = QtGui.QFont('times', 10)

        # Describe menu actions
        show_supplies = QtGui.QAction('Поставки', self)
        show_supplies.triggered.connect(self.open_supply_widget)
        show_raws = QtGui.QAction('Сырье', self)
        show_raws.triggered.connect(self.option_raws)
        show_supplier = QtGui.QAction('Поставщики', self)
        show_supplier.triggered.connect(self.option_supplier)
        show_productions = QtGui.QAction('Выпуск продукции', self)
        show_productions.triggered.connect(self.create_production_widget)
        new_product = QtGui.QAction('Новый продукт', self)
        show_product = QtGui.QAction('Просмотр продуктов', self)
        new_order = QtGui.QAction('Новый заказ', self)
        show_order = QtGui.QAction('Просмотр заказов', self)

        # create menuBar and add actions to menu
        menu = self.menuBar()
        menu.setFont(self.font)
        menu_supply = menu.addMenu('Поставка сырья')
        menu_supply.setFont(self.font)
        menu_supply.addAction(show_supplies)
        menu_supply.addAction(show_raws)
        menu_supply.addAction(show_supplier)
        menu_production = menu.addMenu('Производство')
        menu_production.setFont(self.font)
        menu_production.addAction(show_productions)
        menu_production.addAction(new_product)
        menu_production.addAction(show_product)
        menu_order = menu.addMenu('Заказы')
        menu_order.setFont(self.font)
        menu_order.addAction(new_order)
        menu_order.addAction(show_order)

        # Widget for supplies
        self.s_widget = QtWidgets.QWidget(self)
        self.s_close_button = QtWidgets.QPushButton('Закрыть')
        self.s_update_button = QtWidgets.QPushButton('Обновить')
        self.s_new_button = QtWidgets.QPushButton('Создать')
        self.s_title = QtWidgets.QLabel()
        # Create Model and TableView
        self.model = QtGui.QStandardItemModel()
        self.main_table = QtWidgets.QTableView()
        self.main_table.setModel(self.model)
        # Create Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self.s_widget)
        self.h_layout = QtWidgets.QHBoxLayout(self.s_widget)
        # Add components to Horizontal layout
        self.h_layout.addWidget(self.s_title)
        self.h_layout.addStretch()
        self.h_layout.addWidget(self.s_new_button)
        self.h_layout.addWidget(self.s_update_button)
        self.h_layout.addWidget(self.s_close_button)

        # Widget for productions
        self.p_widget = QtWidgets.QWidget(self)
        self.p_title = QtWidgets.QLabel()
        self.p_close_button = QtWidgets.QPushButton('Закрыть')
        self.p_update_button = QtWidgets.QPushButton('Обновить')
        self.p_new_button = QtWidgets.QPushButton('Создать')
        # Create Model and TableView
        self.model_production = QtGui.QStandardItemModel()
        self.table_production = QtWidgets.QTableView()
        self.table_production.setModel(self.model_production)
        # Main layout
        self.v_layout_production = QtWidgets.QVBoxLayout(self.p_widget)
        # Horizontal layout
        self.h_layout_production = QtWidgets.QHBoxLayout(self.p_widget)
        self.h_layout_production.addWidget(self.p_title)
        self.h_layout_production.addStretch()
        self.h_layout_production.addWidget(self.p_new_button)
        self.h_layout_production.addWidget(self.p_update_button)
        self.h_layout_production.addWidget(self.p_close_button)

        # Widget for orders
        self.o_widget = None

        self.stacked = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.stacked.addWidget(self.s_widget)
        self.stacked.addWidget(self.p_widget)
        self.show_s = False
        self.show_p = False

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
    def option_supplier(self):
        """Вызов окна просмотра, добавления поставщика"""

        self.show_supplier = ShowSupplierWindow(self.connect)
        self.show_supplier.show()
        self.show_supplier.update_getting_supplier()

    @QtCore.Slot()
    def option_raws(self):
        """Вызов окна просмотра всего сырья"""

        self.show_raws = ShowRawWindow(self.connect)
        self.show_raws.show()
        self.show_raws.update_getting_raw()

    @QtCore.Slot()
    def close_widget(self):
        self.s_widget.setVisible(False)
        self.show_s = False

        if self.show_p:
            self.p_widget.setVisible(True)

    @QtCore.Slot()
    def close_p_widget(self):
        self.p_widget.setVisible(False)
        self.show_p = False

        if self.show_s:
            self.s_widget.setVisible(True)

    @QtCore.Slot()
    def open_supply_widget(self):
        if self.p_widget.isVisible():
            self.show_p = True
            self.p_widget.setVisible(False)

        self.s_widget.setVisible(True)

        self.s_close_button.clicked.connect(self.close_widget)

        # Clear model
        self.model.setRowCount(0)

        # Add components to Main layout
        self.main_layout.addLayout(self.h_layout)
        self.main_layout.addWidget(self.main_table)

        # Fill table with data
        self.fill_supply_widget()

    def fill_supply_widget(self):

        font = QtGui.QFont('times', 18)
        self.s_title.setText('Текущие поставки')
        self.s_title.setFont(font)

        cur = self.connect.cursor()
        cur.execute(
            '''select 
                sp.supply_number, 
                sp.supply_date,
                s.supplier_name,
                sp.supply_sum
            from supply sp
            inner join supplier s on sp.supplier_id = s.supplier_id;'''
        )
        result = cur.fetchall()
        cur.close()

        self.model.setHorizontalHeaderItem(0, QtGui.QStandardItem('Номер'))
        self.model.setHorizontalHeaderItem(1, QtGui.QStandardItem('Дата'))
        self.model.setHorizontalHeaderItem(2, QtGui.QStandardItem('Поставщик'))
        self.model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Сумма поставки'))
        self.main_table.verticalHeader().hide()

        row_index = 0

        for i in result[::-1]:
            self.model.insertRow(
                row_index,
                [
                    QtGui.QStandardItem(str(i[0])),
                    QtGui.QStandardItem(i[1].strftime("%m/%d/%Y")),
                    QtGui.QStandardItem(str(i[2])),
                    QtGui.QStandardItem(str(i[3]))
                ])

        self.main_table.setColumnWidth(1, 160)
        self.main_table.setColumnWidth(2, 250)
        self.main_table.setColumnWidth(3, 200)

    @QtCore.Slot()
    def create_production_widget(self):
        if self.s_widget.isVisible():
            self.show_s = True
            self.s_widget.setVisible(False)

        self.p_widget.setVisible(True)
        self.p_widget.resize(self.s_widget.width(), self.s_widget.height())

        # Clear model
        self.model_production.setRowCount(0)

        # Add components to Main layout
        self.v_layout_production.addLayout(self.h_layout_production)
        self.v_layout_production.addWidget(self.table_production)

        self.p_close_button.clicked.connect(self.close_p_widget)

        # Fill table with data
        self.fill_production_widget()

    def fill_production_widget(self):
        font = QtGui.QFont('times', 18)
        self.p_title.setText('Выпуск готовой продукции')
        self.p_title.setFont(font)

        cur = self.connect.cursor()
        cur.execute(
            '''select 
                    p.production_id, 
                    p.production_date 
                from production p;
            '''
        )
        result = cur.fetchall()
        cur.close()

        self.model_production.setHorizontalHeaderItem(0, QtGui.QStandardItem('ID'))
        self.model_production.setHorizontalHeaderItem(1, QtGui.QStandardItem('Дата выпуска'))
        self.table_production.verticalHeader().hide()

        row_index = 0

        for i in result[::-1]:
            self.model_production.insertRow(
                row_index,
                [
                    QtGui.QStandardItem(str(i[0])),
                    QtGui.QStandardItem(i[1].strftime("%m/%d/%Y"))
                ])

        self.table_production.setColumnWidth(1, 160)

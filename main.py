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

    if connect:
        print("Подключение установлено")

        font = QtGui.QFont('times', 18)
        widget.title.setText('Текущие поставки')
        widget.title.setFont(font)

        cur = connect.cursor()
        cur.execute(
            '''select 
                sp.supply_number, 
                sp.supply_date, 
                r.raw_name,
                s.supplier_name,
                sp.supply_sum
            from supply sp
            inner join supplier s on sp.supplier_id = s.supplier_id
            inner join supply_raw sr on sr.supply_id = sp.supply_id 
            inner join raw r on r.raw_id = sr.raw_id;'''
            )
        result = cur.fetchall()
        cur.close()

        widget.model.setHorizontalHeaderItem(0, QtGui.QStandardItem('Номер'))
        widget.model.setHorizontalHeaderItem(1, QtGui.QStandardItem('Дата'))
        widget.model.setHorizontalHeaderItem(2, QtGui.QStandardItem('Наименование сырья'))
        widget.model.setHorizontalHeaderItem(3, QtGui.QStandardItem('Поставщик'))
        widget.model.setHorizontalHeaderItem(4, QtGui.QStandardItem('Сумма поставки'))
        widget.main_table.verticalHeader().hide()

        row_index = 0

        for i in result[::-1]:
            widget.model.insertRow(
                row_index,
                [
                    QtGui.QStandardItem(str(i[0])),
                    QtGui.QStandardItem(i[1].strftime("%m/%d/%Y")),
                    QtGui.QStandardItem(str(i[2])),
                    QtGui.QStandardItem(str(i[3])),
                    QtGui.QStandardItem(str(i[4]))
                 ])

        widget.main_table.setColumnWidth(1, 120)
        widget.main_table.setColumnWidth(2, 200)
        widget.main_table.setColumnWidth(3, 200)
        widget.main_table.setColumnWidth(4, 180)

    sys.exit(app.exec())


if __name__ == '__main__':
    confectionary()

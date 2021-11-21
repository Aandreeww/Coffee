import sys, random, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PyQt5.QtGui import QPainter, QColor


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('cof_tbl.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Кофе')
        self.select_data()

    def select_data(self):
        res = []
        all = self.connection.cursor().execute("""SELECT * FROM all_cof""").fetchall()
        for i in all:
            res.append((i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.setHorizontalHeaderLabels(['id', 'Название сорта', 'степень обжарки',
                                                    'молотый/в зернах', 'описание вкуса', 'цена', 'объем упаковки'])


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
import sys, random, sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QWidget
from PyQt5.QtGui import QPainter, QColor


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi('cof_tbl.ui', self)
        self.connection = sqlite3.connect("coffee.sqlite")
        self.setWindowTitle('Кофе')
        self.pushButton.clicked.connect(self.open_ed)
        self.update.clicked.connect(self.select_data)
        self.select_data()

    def open_ed(self):
        rows = list(set([i.row() for i in self.tableWidget.selectedItems()]))
        ids = [self.tableWidget.item(i, 0).text() for i in rows]
        if len(ids) == 0:
            ids = ['', '']
        self.ed = Editer(self, ids[0])
        self.ed.show()

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


class Editer(QWidget):
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.initUI(args)

    def initUI(self, args):
        self.sel = args[0]
        self.id = args[1]
        self.setWindowTitle('Добавление и удаление')
        self.connection = sqlite3.connect("coffee.sqlite")
        self.adder.clicked.connect(self.add_game)
        self.rename.clicked.connect(self.changed)

    def add_game(self):
        cur = self.connection.cursor()
        cur.execute('''INSERT INTO all_cof(name, ro_degree, type, taste, price, size)
        VALUES(?, ?, ?, ?, ?, ?)''', (self.name.text(),
                                   self.roasting.text(),
                                   self.type.text(),
                                   self.taste.text(),
                                   int(self.cost.text()),
                                   int(self.vol.text())))
        self.connection.commit()

    def changed(self):
        if self.id == '':
            self.sel.statusBar().showMessage(f'Вы должны выбрать кофе')
            self.sel.statusBar().setStyleSheet('background:green')
            Editer.setVisible(self, False)
        else:
            req = []
            if self.name.text() != '':
                req.append(f'SET name = "{self.name.text()}"')
            if self.roasting.text() != '':
                req.append(f'SET ro_degree = "{self.roasting.text()}"')
            if self.taste.text() != '':
                req.append(f'SET type = "{self.type.text()}"')
            if self.taste.text() != '':
                req.append(f'SET taste = "{self.taste.text()}"')
            if self.cost.text() != '':
                req.append(f'SET price = {int(self.cost.text())}')
            if self.vol.text() != '':
                req.append(f'SET size = {int(self.vol.text())}')
            for i in range(len(req)):
                cur = self.connection.cursor()
                que = "UPDATE all_cof\n"
                que += req[i] + '\n'
                que += f"WHERE id = {self.id}"
                cur.execute(que)
                self.connection.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MyWidget()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
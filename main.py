import sys,pyqtgraph as pg
import random
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow,QComboBox, QLabel,QPushButton,QGraphicsView,QGraphicsScene,QTableView)
from PyQt5.uic import loadUi
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

class UI(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("form.ui", self)
        self.signalsAndslots()
        self.show()
    def signalsAndslots(self):
        # initialize Qvar# import sys,pyqtgraph as pg
        self.epsText=self.findChild(QLineEdit,"LEeps")
        self.lowboundText=self.findChild(QLineEdit,"LElowbound")
        self.upboundText=self.findChild(QLineEdit,"LEupbound")
        self.maxiterText=self.findChild(QLineEdit,"LEmaxiter")
        self.filepathText=self.findChild(QLineEdit,"LEfilepath")
        self.estimatedrootLabel=self.findChild(QLabel,'Lestimatedroot')
        self.exactrootLabel=self.findChild(QLabel,'Lexactroot')
        self.readfile=self.findChild(QPushButton,"BTreadfile")
        self.compute=self.findChild(QPushButton,"BTcompute")
        self.combomethod=self.findChild(QComboBox,"CBmethods")
        self.graphit=self.findChild(QGraphicsView,"graphicsView")
        self.tableit=self.findChild(QTableView,"tableView")
        # assign functionality
        self.compute.clicked.connect(self.computepushed)
        self.readfile.clicked.connect(self.parseit)
        self.combomethod.currentIndexChanged.connect(self.comboboxchanged)
        self.scene = QGraphicsScene()
        self.graphit.setScene(self.scene)
    def comboboxchanged(self):
        if self.combomethod.currentText() in ['Bisection Method','Regula Falsi Method','Secant Method']:
            self.upboundText.setDisabled(False)
        else:
            self.upboundText.setDisabled(True)
    def computepushed(self):
        theTitle = "pyqtgraph plot"
        y=[]
        plotted = pg.PlotWidget()
        self.scene.clear()
        for _ in range(100):
            y.append(random.randint(0,100))
        x = range(0, 100)
        plotted.plot(x, y, title=theTitle, pen='r')
        plotted.showGrid(x=True, y=True)
        self.scene.addWidget(plotted)
        data = [[11, 12, 13, 14, 15],
                [21, 22, 23, 24, 25],
                [31, 32, 33, 34, 35]]

        self.model =TableModel(data)
        self.tableit.setModel(self.model)

    def run(self):
        pass
    def parseit(self):
        pass
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UI()
    win.show()
    sys.exit(app.exec())
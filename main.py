import sys,pyqtgraph as pg
from csv import reader
from PyQt5.QtWidgets import (QApplication, QLineEdit, QMainWindow,QComboBox,QLabel,
QPushButton,QGraphicsView,QGraphicsScene,QTableView,QTextEdit,QRadioButton,QCheckBox)
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
        self.func=self.findChild(QLineEdit,"LEfunc")
        self.estimatedrootLabel=self.findChild(QLabel,'Lestimatedroot')
        self.exactrootLabel=self.findChild(QLabel,'Lexactroot')
        self.readfile=self.findChild(QPushButton,"BTreadfile")
        self.compute=self.findChild(QPushButton,"BTcompute")
        self.combomethod=self.findChild(QComboBox,"CBmethods")
        self.graphit=self.findChild(QGraphicsView,"graphicsView")
        self.tableit=self.findChild(QTableView,"tableView")
        self.messages = self.findChild(QTextEdit, "TEmessages")
        self.fastmode = self.findChild(QRadioButton, "RBfastmode")
        self.stepmode = self.findChild(QRadioButton, "RBstepmode")
        self.isreadfile = self.findChild(QCheckBox, "CBisread")
        # assign functionality
        self.isreadfile.stateChanged.connect(self.alterstate)
        self.compute.clicked.connect(self.computepushed)
        self.readfile.clicked.connect(self.parseit)
        self.combomethod.currentIndexChanged.connect(self.comboboxchanged)
        self.scene = QGraphicsScene()
        self.graphit.setScene(self.scene)
        self.tableit.doubleClicked.connect(self.rowselect)
        self.filepathText.setDisabled(True)
        self.readfile.setDisabled(True)
    def comboboxchanged(self):
        if self.combomethod.currentText() in ['Bisection Method','Regula Falsi Method','Secant Method']:
            self.upboundText.setDisabled(False)
        else:
            self.upboundText.setDisabled(True)
    def computepushed(self):
        self.messages.setText('')
        try:
            ub=''
            if self.epsText.text()=='':
                self.messages.setText('Please fill the eps field!')
                return
            else:
                eps = float(self.epsText.text())
                if eps<1e-5:
                    eps=1e-5
                    self.epsText.setText('1e-5')
                elif eps>1e-1:
                    eps=1e-1
                    self.epsText.setText('1e-1')
            if self.func.text()=='':
                self.messages.append('Please fill the function field!')
                return
            else:
                func = self.func.text()
            if self.maxiterText.text()=='':
                self.messages.append('Please fill the Max iteration field!')
                return
            else:
                it = int(self.maxiterText.text())
                if it < 1:
                    it = 1
                    self.maxiterText.setText('1')
                elif it > 50:
                    it = 50
                    self.maxiterText.setText('50')
            if self.lowboundText.text()=='':
                self.messages.append('Please fill the low bound field!')
                return
            else:
                lb=float(self.lowboundText.text())
            if self.upboundText.isEnabled():
                if self.upboundText.text()=='' :
                    self.messages.append('Please fill the up bound field!')
                    return
                else:
                    ub=float(self.upboundText.text())

            self.run(func,ub,lb,eps,it)

        except:
            self.messages.setText('unable to read input...check your inputs!')
    def alterstate(self):
        if self.isreadfile.isChecked():
            self.upboundText.setDisabled(True)
            self.lowboundText.setDisabled(True)
            self.func.setDisabled(True)
            self.epsText.setDisabled(True)
            self.maxiterText.setDisabled(True)
            self.upboundText.setDisabled(True)
            self.combomethod.setDisabled(True)
            self.filepathText.setEnabled(True)
            self.readfile.setDisabled(False)
            self.compute.setDisabled(True)
        else:
            self.upboundText.setDisabled(False)
            self.lowboundText.setDisabled(False)
            self.func.setDisabled(False)
            self.epsText.setDisabled(False)
            self.maxiterText.setDisabled(False)
            self.upboundText.setDisabled(False)
            self.combomethod.setDisabled(False)
            self.filepathText.setDisabled(True)
            self.readfile.setDisabled(True)
            self.compute.setDisabled(False)
            self.tabling([[]])
            self.messages.setText('')
            self.filepathText.setText('')
            self.scene.clear()
    def run(self,fun,upbound,lowbound,eps=1e-5,maxit=50,method=None):
        plotted = pg.PlotWidget()
        self.scene.clear()
        # x,y=,
        plotted.plot(x, y, pen='r')
        plotted.showGrid(x=True, y=True)
        self.scene.addWidget(plotted)
    def rowselect(self):
            ind=self.tableit.selectionModel().selectedRows()[0].row()
            self.run(self.data[ind][0],self.data[ind][1],self.data[ind][2],self.data[ind][3],self.data[ind][4],self.data[ind][5])
    def csvreader(self,filename):
        try:
            data = []
            with open(filename, 'r', encoding='unicode_escape') as read_obj:
                csv_reader = reader(read_obj)
                data = list(csv_reader)
            return data
        except:
            self.messages.setText('unable to read file, please check your file/path')
    def parseit(self):
        path=self.filepathText.text()
        if path=="":
            self.messages.setText('Please enter filepath')
            return
        try:
            self.data=self.csvreader(path)
            self.tabling(self.data)
            self.messages.setText('Double click on row to process given data!')

        except:
            self.messages.setText('unable to parse data...check your file')

    def tabling(self,data):
        self.model =TableModel(data)
        self.tableit.setModel(self.model)
        self.tableit.resizeColumnsToContents()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = UI()
    win.show()
    sys.exit(app.exec())



import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import pandas as pd


class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        data = pd.DataFrame([
          [1, 9, 2],
          [1, 0, -1],
          [3, 5, 2],
          [3, 3, 2],
          [5, 8, 9],
        ])
        data.columns = ['A', 'B', 'C']
        # mas = []
        #
        # for num in range(len(data)):
        #     mas.append(num + 1)
        data.index=list(range(1,len(data)+1))
        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

    def getVertHead(self):
        mas = []
        rowsCount=len(self.da)
        for num in range(rowsCount):
            mas.append(num + 1)
        return mas
app=QtWidgets.QApplication(sys.argv)
window=MainWindow()
window.show()
app.exec_()
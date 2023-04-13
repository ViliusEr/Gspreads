import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from datetime import datetime
import pandas as pd
from myGspread import googleSheetData

class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, values,header):
        super(TableModel, self).__init__()
        self._data = pd.DataFrame(data=values,columns=header)

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        if orientation == Qt.Vertical:
            return str(self._data.index[col])
        return None

    #
    #
    #
    # def data(self, index, role):
    #     if role == Qt.DisplayRole:
    #         # Get the raw value
    #         value = self._data[index.row()][index.column()]
    #
    #         # Perform per-type checks and render accordingly.
    #         if isinstance(value, datetime):
    #             # Render time to YYY-MM-DD.
    #             return value.strftime("%Y-%m-%d")
    #
    #         if isinstance(value, float):
    #             # Render float to 2 dp
    #             return "%.2f" % value
    #
    #         if isinstance(value, str):
    #             # Render strings with quotes
    #             return '"%s"' % value
    #
    #         # Default (anything not captured above: e.g. int)
    #         return value
    #     if role == Qt.TextAlignmentRole:
    #         value = self._data[index.row()][index.column()]
    #
    #         if isinstance(value, int) or isinstance(value, float) or isinstance(value,datetime):
    #             # Align right, vertical middle.
    #             return Qt.AlignVCenter + Qt.AlignRight
    #
    # def rowCount(self, index):
    #     # The length of the outer list.
    #     return len(self._data)
    #
    # def columnCount(self, index):
    #     # The following takes the first sub-list, and returns
    #     # the length (only works if all rows are an equal length)
    #     return len(self._data[0])
    #
    # def headerData(self, col, orientation, role):
    #     if orientation == Qt.Horizontal and role == Qt.DisplayRole:
    #         return self._data.columns[col]
    #     return None
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = QtWidgets.QTableView()

        # data = [
        #     [4, 9, 2],
        #     [1, -1, 'hello'],
        #     [3.023, 5, -5],
        #     [3, 3, datetime(2017, 10, 1)],
        #     [7.555, 8, 9],
        # ]
        # # data=getValues()

        headers=['Eil. Nr.', 'Vardas', 'Pavarde', 'Pacientas']
        values=[
            ['1', 'new_value', 'DVINSKICH', 'DVINSKICH new_value'],
            ['2', 'Edvardas', 'DOROŠKEVIČIUS', 'DOROŠKEVIČIUS Edvardas'],
            ['3', 'Pranas', 'GAILIŪNAS', 'GAILIŪNAS Pranas'],
            ['4', 'Vitalijus', 'MURNIKOVAS', 'MURNIKOVAS Vitalijus'],
            ['5', 'Eugenijus', 'BIMBA', 'BIMBA Eugenijus'],
            ['6', 'Algis', 'ŽIGOTA', 'ŽIGOTA Algis']
        ]


        self.model = TableModel(headers,values)
        self.model=TableModel(h)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)

if __name__ == '__main__':
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    app.exec_()
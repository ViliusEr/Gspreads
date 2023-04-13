import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
# from myGspread import getRecords, getColumns, getValues
from myGspread import googleSheetData

# df = pd.DataFrame({'Vardas': ['Mary', 'Jim', 'John'],
#                    'Skaičius': [100, 200, 300],
#                    'Raidė': ['a', 'b', 'c']})


gs =  googleSheetData()
# tbl_data = gs.getValues()
# # tbl_headers = sum(getColumns(), [])
# tbl_headers = gs.getColumns()
# df = pd.DataFrame(data=tbl_data,columns=tbl_headers )

df = pd.DataFrame(gs.getRecords())
df.index=list(range(1,len(df)+1))
# df.index=['1','2','3','4','5']

class pandasModel(QAbstractTableModel):

    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        # if orientation == Qt.Horizontal and role == Qt.DisplayRole:
        #     return self._data.columns[col]
        # return None

        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[col])

            if orientation == Qt.Vertical:
                return str(self._data.index[col])
        return None
        # if orientation == Qt.Horizontal:
        #     return str(self._data.columns[col])
        #
        # if orientation == Qt.Vertical:
        #     return str(self._data.index[col])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    model = pandasModel(df)
    view = QTableView()
    view.setModel(model)
    view.resize(800, 600)
    view.show()
    sys.exit(app.exec_())

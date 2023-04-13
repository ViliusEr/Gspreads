# -*- coding: utf-8 -*-

from myGspread import googleSheetData
from PandasTable import pandasModel
import pandas as pd
from Frm import Ui_MainWindow
from PyQt5 import  QtWidgets


class myForma(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def loadData(self):
        gs= googleSheetData()
        data=gs.getRecords()
        df=pd.DataFrame(data)
        # df.columns=gs.getColumns()
        df.index=list(range(1,len(df)+1))
        model=pandasModel(df)
        self.tableView.setModel(model)

    def copyText(self, item):
        celValue=item.data()

        self.textEdit.setText(celValue)

    def connectEvents(self):
        self.tableLoadButton.clicked.connect(self.loadData)
        self.tableView.pressed.connect(self.copyText)
        # self.tableView.selectionModel().selectionChanged.connect(self.on_selectionChanged)                                                #  selectionMode().selectionChanged.connect(self.on_selectionChanged)

    # def on_selectionChanged(self, selected, deselected):
    #
    #     for ix in selected.indexes():
    #         print('Selected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))
    #
    #     for ix in deselected.indexes():
    #         print('Deselected Cell Location Row: {0}, Column: {1}'.format(ix.row(), ix.column()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = myForma()
    ui.setupUi(MainWindow)
    ui.connectEvents()
    MainWindow.show()
    sys.exit(app.exec_())
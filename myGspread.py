import gspread

# from google.oauth2.service_account import Credentials
# import pandas as pd
# import numpy as np

spreadKey = '1oQwjv5YwyNytc2jtzlpmShOxOHTRS04uUi8-dNiwZJ4'
# sheetName = 'Pacient'
sheetName = 'Zurn'
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

gs = gspread.service_account(filename='creds.json', scopes=scopes)
sh = gs.open_by_key(spreadKey)

# credentials = Credentials.from_service_account_file(
#     'creds.json',
#     scopes=scopes
# )

# gc = gspread.authorize(credentials)
# sh=gc.open_by_key(spreadKey)
wsh = sh.worksheet(sheetName)
val = wsh.get_all_values()
columns = val.pop(0)


class googleSheetData():
    def getRecords(self):
        return wsh.get_all_records()

    # records=wsh.get_all_records()
    # print(records)

    def getValues(self):
        # return pd.DataFrame(val).values.tolist()
        return val

    def getColumns(self):
        return columns
        # return pd.DataFrame(columns).values.tolist()

    def getRowVal(rowNum):
        return wsh.row_values(rowNum)


if __name__ == '__main__':
    gs = googleSheetData()
    print(gs.getColumns())
    print(gs.getValues())
    print(len(gs.getRecords()))


import gspread  # импортируем gspread
from oauth2client.service_account import ServiceAccountCredentials  # ипортируем ServiceAccountCredentials
import pprint  # импортируем pprint
import numpy as np

link = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
my_creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json',link)  # формируем данные для входа из нашего json файла
client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
sheet = client.open_by_key('1oQwjv5YwyNytc2jtzlpmShOxOHTRS04uUi8-dNiwZJ4').worksheet('Zurn')                      # .sheet1  открываем нужную на таблицу и лист
print_p = pprint.PrettyPrinter()  # описываем прити принт

get_data = sheet.get_all_records()  # получаем все данные из таблици
get_data1 = sheet.row_values(2)  # получаем данные ряда
get_data2 = sheet.col_values(2)  # получаем данные колонки
get_data3 = sheet.cell(2, 2).value  # получаем данные ячейки
print("get_data ")  # выводми в консоль текст get_data
print_p.pprint(get_data)  # выводми в консоль значение get_data
print("get_data1 ")  # выводми в консоль текст get_data1
print_p.pprint(get_data1)  # выводми в консоль значение get_data1
print("get_data2 ")  # выводми в консоль текст get_data2
print_p.pprint(get_data2)  # выводми в консоль значение get_data2
print("get_data3 ")  # выводми в консоль текст get_data3
print_p.pprint(get_data3)  # выводми в консоль значение get_data3

sheet.update_cell(2, 2, "new_value")  # меняем значение ячейки
get_data5 = sheet.cell(2, 2).value  # получаем данные ячейки
print("get_data5 ")  # выводми в консоль текст get_data5
print_p.pprint(get_data5)  # выводми в консоль значение get_data5
print_p.pprint(np.array(get_data))
print(type(get_data))
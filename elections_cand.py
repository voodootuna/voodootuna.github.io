# -*- coding: utf-8 -*-
import xlrd
import json

historical_data = {}

file_path = './candidats.xlsx'
workbook = xlrd.open_workbook(file_path)




candidates_data = {}

def scrapworksheet(n):
	sheet = workbook.sheet_by_index(n)
	nrows = sheet.nrows

	data = []
	for row in range(1, nrows):
		cell_0 = sheet.cell(row, 0).value or ''
		cell_1 = sheet.cell(row, 1).value or ''
		cell_2 = sheet.cell(row, 2).value or ''
		cell_3 = sheet.cell(row, 3).value  or ''
		cell_4 = sheet.cell(row, 4).value or ''
		cell_5 = sheet.cell(row, 5).value or ''
		cell_6 = sheet.cell(row, 6).value or ''

		data.append({"name": cell_0,
						"age":cell_1,
						"party":cell_2,
						"prof":cell_3,
						"addr":cell_4,
						"com":cell_5,
						"icon_name":cell_6
					})
	return data



for i in range(0, 21):
	print(i)
	candidates_data[str(i+1)] = scrapworksheet(i)

print(candidates_data)

with open("./candidates.json", "w") as f:
	#print(save_data)
	json.dump(candidates_data, f)

# -*- coding: utf-8 -*-
import xlrd
import json

historical_data = {}

file_path = './registry_map.xlsx'
workbook = xlrd.open_workbook(file_path)
sheet = workbook.sheet_by_index(0)
nrows = sheet.nrows
print('NUM ROWS', nrows)

def xls_to_json(startrow, circ):
	#print("START ROW",startrow)
	data =[]
	for row in range(startrow, nrows):
		cell_0 = sheet.cell(row, 0).value
		cell_1 = sheet.cell(row, 1).value
		cell_2 = sheet.cell(row, 2).value
		cell_3 = sheet.cell(row, 3).value
		cell_4 = sheet.cell(row, 4).value
		if not cell_0:
			break
		data.append({"no": cell_0,
								 "reg_area":cell_1,
								 "polling_station":cell_2,
								 "electors":cell_3,
								 "map_url":cell_4,

								 })

	historical_data[circ] = data

	

def xls_grouping(sheet):
	print('start')
	

	for row in range(0,nrows):
		cell_0 = sheet.cell(row, 0).value
		if 'circonscription'  in str(cell_0).lower():
			#print(cell_0)
			circ = cell_0.split()[1]
			xls_to_json( row + 1, circ)










xls_grouping(sheet)
json_data = json.dumps(historical_data)
with open('./registry.json','w') as f:
	json.dump(historical_data, f)
print("HISTORICAL DATA JSON", json_data)

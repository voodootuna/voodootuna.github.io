# -*- coding: utf-8 -*-
import xlrd
import json


file_path = './results.xlsx'
workbook = xlrd.open_workbook(file_path)
sheet_names = workbook.sheet_names()



def generateCircDict(year_list):
	circ = 21
	generated_data = {}
	year_dict = {}
	for y in year_list:
		year_dict[y] = None
	for j in range(1, circ+1):
		generated_data[str(j)] = year_dict


	#some kind of issue with generated_data messing with the dict
	with open('./template.json', 'w') as f:
		json.dump(generated_data, f)

	
def map_yearly_data(startrow, circ, sheet, nrows, year):
	data = []
	for row in range(startrow, nrows):
		cell_0 = sheet.cell(row, 0).value or ''
		cell_1 = sheet.cell(row, 1).value or ''
		cell_2 = sheet.cell(row, 2).value or ''
		cell_3 = sheet.cell(row, 3).value  or ''
		cell_4 = sheet.cell(row, 4).value or ''
		cell_5 = sheet.cell(row, 5).value or ''

		data.append({"no": cell_0,
						"name":cell_1,
						"party":cell_2,
						"ethnicity":cell_3,
						"votes":cell_4,
						"perc_votes":cell_5
					})
		#print(data)

		if not sheet.cell(row, 0).value:
			#print("BREAK")
			break
	
	return data
		
		


def scrap_year(sheets_no):
	sheet_names = workbook.sheet_names()
	generateCircDict(sheet_names)
	historical_data = {}
	with open('./template.json', 'r') as f:
		json_data = f.read()
		historical_data = json.loads(json_data)
	print(historical_data)
	for i in range(0, sheets_no):
		print("sheets range", i)
		sheet = workbook.sheet_by_index(i)
		
		nrows = sheet.nrows
		#print("SHEET NAME", sheet_names)
		for row in range(0,nrows):
			cell_0 = sheet.cell(row, 0).value
			if 'circonscription'  in str(cell_0).lower():

				year = sheet_names[i]
				circ = cell_0.split()[1]
				print("CIRCONSCRIPTION", circ)
			
				circ_data = map_yearly_data(row + 1, circ, sheet, nrows, year)
				print('----------------')
				historical_data[circ][year] = circ_data
			else:
				pass

	return historical_data
	





save_data = scrap_year(4)

with open("./results.json", "w") as f:
	#print(save_data)
	json.dump(save_data, f)

print('--------------------------------------')

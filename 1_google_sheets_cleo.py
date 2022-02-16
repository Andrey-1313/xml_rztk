import gspread
import time
import re
from utils.help_func import create_pid

# auth to spreadsheets via Google Sheets API
client = gspread.service_account(filename="65b47311f305.json")

# define spreadsheet and worksheets to write data
sheet1 = client.open('cleo')
sheet_instance = sheet1.get_worksheet(0)
sheet_instance2 = sheet1.get_worksheet(1)
sheet_instance3 = sheet1.get_worksheet(2)

# define spreadsheet to read data from
sheet = client.open('stock')
worksheet_objs = sheet.worksheets()
for worksheet in worksheet_objs:
	rugs=[] # inventory in all size variations
	rugs_models=[] # name of inventory models 
	collectios=[] # name of inv collections

	shname=worksheet.title.capitalize().strip()
	collectios_data=shname,
	collectios.append(collectios_data)

	#define row which contain sizes of rugs (1-st or 2-nd)
	xstr=''
	for x in worksheet.row_values(1):
		xstr+=x
	if re.search(r'\d{3,}', xstr)==None:
		sizes=(worksheet.row_values(2))
	else:
		sizes=(worksheet.row_values(1))

	# list of rugs models in 2-nd column	
	models=(worksheet.col_values(2))

	# find stock value for each model+size
	for model in models[2:]:
		if len(model)>0 and model.startswith('диза')==False:
			print(model)
			data_m=shname, (shname+' '+model)
			rugs_models.append(data_m)
			for size in sizes[2:]:
				#define max sizes column (right boundary of table)
				max_cell=worksheet.find(sizes[-1]).col

				if len(size)>1:
					cell_size = worksheet.find(size)

					#find unique name of the model that is in the boundaries
					cell_model_lst=worksheet.findall(model)
					for item in cell_model_lst:
						if item.col >= max_cell:
							cell_model_lst.pop(cell_model_lst.index(item))
					cell_model = cell_model_lst[0]
					# find stock value for pair model+size
					stock=worksheet.cell(cell_model.row, cell_size.col).value
					#replace '*' and cyrillic 'x' with latin 'x' 
					size=re.sub(r'[\*х]', 'x', size)
					info=(shname+' '+model)
					pid=create_pid(shname, info, size)
					print(shname, info, size, pid)
					data=info, size, stock, pid
					rugs.append(data)
					time.sleep(5) #due to API quota limits
	#write data for each iteration through worksheets in case to prevent losing data after network failure
	time.sleep(5)
	col_val = sheet_instance.col_values(1)
	print_row=len(col_val)+2
	sheet_instance.update('A{}'.format(print_row), rugs)

	col_val_2 = sheet_instance2.col_values(1)
	print_row_2=len(col_val_2)+2
	sheet_instance2.update('A{}'.format(print_row_2), rugs_models)

	col_val_3 = sheet_instance3.col_values(1)
	print_row_3=len(col_val_3)+1
	sheet_instance3.update('A{}'.format(print_row_3), collectios)


The final task is to create `.xml` product feed for rozetka marketplace 

## 1. Read write data from/to Google Sheets
**Used file** `1_google_sheets_r_w.py`

I have a spreadsheet with a lot of worksheets. 
I need to concat cols + rows + value in col/row in order to create lists of products, product models and collections, then write it into another spreadsheet

## 2. Create sqlite database 
**Used file** `2_create_sqlite.py`

I've create database with three tables in order to write products data from new spreadsheet 

## 3. Write data into database 
**Used file** `3_wrtite_to_sqlite_read_sheets.py`

Insert or update data into database from spreadsheet

## 4. Processing data from database and creating xml feed
**Used file** `4_create_xml_rztk.py`

Create xml feed according to the required format

## Utility functions
**files** `utils/help_func.py` and `utils/get_colour.py`

###### Used to:
* create unique digit product id
* read image files names and compare them to product names for linking img 
* analyze RGB img map and define prevailing colors

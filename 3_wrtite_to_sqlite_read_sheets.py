import sqlite3
import gspread
from utils.get_colour import photo_info
from utils.help_func import prepare_item

client = gspread.service_account(filename="65b47311f305.json")

conn = sqlite3.connect('cleopatra.sqlite')
cur = conn.cursor()

#define spreadsheet and worksheets to write data
sheet1 = client.open('cleo')
product_instance = sheet1.get_worksheet(0)
models_instance = sheet1.get_worksheet(1)
collections_instance = sheet1.get_worksheet(2)

#filtering only filled cels
products_list = list(filter(lambda x: len(x['Model'])>0, product_instance.get_all_records()))

models_list = list(filter(lambda x: len(x['Name'])>0, models_instance.get_all_records()))

collections_list = list(filter(lambda x: len(x['Name'])>0, collections_instance.get_all_records()))


for coll in collections_list:
    cur.execute('SELECT * FROM collections WHERE name = ? ', (coll['Name'],))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO collections (name, rztk_name, price, pile_height, material, type, apply, design, features, description, description_ua)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)''',
        (coll['Name'], coll['Назв RZTK'], coll['Цена'], coll['Высота ворса, см'],
        coll['Состав'], coll['Тип'], coll['Назначение'], coll['Дизайн'], coll['Доп характеристики'], coll['Описание Рус'], coll['Опис УКР']))
    else:
        cur.execute('''UPDATE collections SET rztk_name=?, price=?,
                        pile_height=?, material=?, type=?, apply=?, design=?, features=?, description=?, description_ua=? WHERE name=?''',
                        (coll['Назв RZTK'], coll['Цена'], coll['Высота ворса, см'], coll['Состав'],
                        coll['Тип'], coll['Назначение'], coll['Дизайн'], coll['Доп характеристики'], coll['Описание Рус'], coll['Опис УКР'], coll['Name']))
    conn.commit() 

for model in models_list:
    cur.execute('SELECT * FROM models WHERE name = ? ', (model['Name'],))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO models (name, coll_id, form, colours, img)
        VALUES (?,(SELECT id FROM collections WHERE name=?),'Прямоугольная',?,?)''',
        (model['Name'], model['Coll'], photo_info('Photo', prepare_item(model['Name']))[0], photo_info('Photo', prepare_item(model['Name']))[1]))
    else:
        cur.execute('''UPDATE models SET coll_id=(SELECT id FROM collections WHERE name=?), form='Прямоугольная', colours=?, img=? WHERE name=?''',
                        (model['Coll'], photo_info('Photo', prepare_item(model['Name']))[0], photo_info('Photo', prepare_item(model['Name']))[1], model['Name']))
    conn.commit() 

for item in products_list:
    cur.execute('SELECT * FROM products WHERE prod_id = ? ', (item['Prod_id'],))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO products (prod_id, model_id, size, qty)
        VALUES (?,(SELECT id FROM models WHERE name=?),?,?)''',
        (item['Prod_id'], item['Model'], item['Size'], item['Qty']))
    else:
        cur.execute('''UPDATE products SET qty=? WHERE prod_id=?''',
                        (item['Qty'], item['Prod_id']))
    conn.commit() 

cur.close()


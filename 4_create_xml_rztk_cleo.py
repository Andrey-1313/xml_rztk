from datetime import datetime
from lxml import etree
import sqlite3


conn = sqlite3.connect('cleopatra.sqlite')
cur = conn.cursor()

cur.execute('''SELECT prod_id, collections.name, collections.rztk_name, models.name, 
                size, qty, price, pile_height, material, type, apply, design, features, description, description_ua, form, colours, img
                FROM products
                JOIN models ON products.model_id=models.id
                JOIN collections ON models.coll_id=collections.id
                WHERE qty!='' AND price !='' ''') 
row = cur.fetchall()
cur.close()

today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

root = etree.Element("yml_catalog", date=str(today))
shop = etree.SubElement(root, 'shop')
name = etree.SubElement(shop, 'name')
name.text = 'Oriental Carpets'

company = etree.SubElement(shop, 'company')
company.text='ТОВ «Клеопатра Інтернешнл Трейдінг Компані»'
currencies = etree.SubElement(shop, 'currencies')
currency = etree.SubElement(currencies, 'currency', id="UAH", rate="1")


categories = etree.SubElement(shop, 'categories')
category = etree.SubElement(categories, 'category', id='1', rz_id="142254")
category.text='Килими'
offers = etree.SubElement(shop, 'offers')


for data in row:
    prod_id, coll_name, rztk_name, model_name, size, qty, price, pile, material, type_c, apply_c, design, features, description, description_ua, form, colours, img_links = data


    name_ua = model_name.replace(coll_name, rztk_name)
    name_ru=name_ua.replace('і', 'и')

    title='Ковер '+name_ru+' '+size
    title_ua='Килим '+name_ua+' '+size

    if type_c=='Безворсовые':
        title='Безворсовый ковер '+name_ru+' '+size
        title_ua='Безворсовий килим '+name_ua+' '+size

    if type_c=='Ворсистые (шагги)':
        title='Ковер с высоким ворсом '+name_ru+' '+size
        title_ua='Килим з високим ворсом '+name_ua+' '+size

    if type_c=='Из вискозы':
        title='Ковер из вискозы '+name_ru+' '+size
        title_ua='Килим з віскози '+name_ua+' '+size


    width=float(size.split('x')[0])/100
    length=float(size.split('x')[1])/100
    prod_price=0
    prod_price=round(width*length*int(price.split(';')[0]))

    if coll_name=='Fortuna' and width<=1.2:
        prod_price=round(width*length*int(price.split(';')[1]))

    if coll_name=='Erin' and width<=1.2:
        prod_price=round(width*length*int(price.split(';')[1]))

    if coll_name=='Symphony' and width<1.2:
        prod_price=round(width*length*int(price.split(';')[1]))

    if coll_name=='Marseille' and width<=1.2:
        prod_price=round(width*length*int(price.split(';')[1]))


    available='true'
    if int(qty)==0 or img_links is None:
        available='false'

    print(title+'....'+title_ua)


    if float(width)>=0.5 and float(width)<=0.8:
        valueid='138242'
        width_text='0.5 - 0.8 м'
    if float(width)>0.8 and float(width)<=1.2:
        valueid='138247'
        width_text='0.9 - 1.2 м'
    if float(width)>1.2 and float(width)<=1.5:
        valueid='138252'
        width_text='1.3 - 1.5 м'
    if float(width)>1.5 and float(width)<=1.8:
        valueid='138257'
        width_text='1.6 - 1.8 м'
    if float(width)>1.8 and float(width)<=2.3:
        valueid='138262'
        width_text='1.9  - 2.3 м'
    if float(width)>2.3 and float(width)<=2.6:
        valueid='138267'
        width_text='2.4  - 2.6 м'


    if float(length)>=0.5 and float(length)<=1.0:
        valueid_l='138202'
        length_text='0.5 - 1 м'
    if float(length)>1.0 and float(length)<=1.5:
        valueid_l='138207'
        length_text='1.1 - 1.5 м'
    if float(length)>1.5 and float(length)<=2.0:
        valueid_l='138212'
        length_text='1.6 - 2 м'
    if float(length)>2.0 and float(length)<=2.5:
        valueid_l='138217'
        length_text='2.1 - 2.5 м'
    if float(length)>2.5 and float(length)<=3.0:
        valueid_l='138222'
        length_text='2.6 - 3 м'
    if float(length)>3.0 and float(length)<=3.5:
        valueid_l='138227'
        length_text='3.1 - 3.5 м'
    if float(length)>3.5 and float(length)<=4.0:
        valueid_l='138232'
        length_text='3.6 - 4 м'
    if float(length)>4.0:
        valueid_l='138237'
        length_text='более 4 м'


    offer = etree.SubElement(offers, 'offer', id=str(prod_id), available=available)
    price_p = etree.SubElement(offer, 'price')
    price_p.text = str(prod_price)

    stock_quantity = etree.SubElement(offer, 'stock_quantity')
    stock_quantity.text = qty
    currencyId = etree.SubElement(offer, 'currencyId')
    currencyId.text = 'UAH'
    categoryId = etree.SubElement(offer, 'categoryId')
    categoryId.text = '1'
    if img_links is not None and len(img_links)>1:
        images=img_links.split(';')
        for i in images:
            picture=etree.Element('picture')
            offer.insert(5+images.index(i),picture)
            picture.text=i
    name_r = etree.SubElement(offer, 'name')
    name_r.text = title
    name_ua_r = etree.SubElement(offer, 'name_ua')
    name_ua_r.text = title_ua
    vendor = etree.SubElement(offer, 'vendor')
    vendor.text = 'Oriental Weavers'
    description_r = etree.SubElement(offer, 'description')
    description_r.text = etree.CDATA(description)
    description_r_ua = etree.SubElement(offer, 'description_ua')
    description_r_ua.text = etree.CDATA(description_ua)

    width_r = etree.SubElement(offer, 'param', name='Ширина', paramid='53697', valueid=valueid)
    width_r.text = width_text
    length_r = etree.SubElement(offer, 'param', name='Длина', paramid='53692', valueid=valueid_l)
    length_r.text = length_text
    
    sizes_r = etree.SubElement(offer, 'param', name='Размеры', paramid='73068')
    sizes_r.text = str(width).rstrip('.0')+' x '+str(length).rstrip('.0')+' м'
    country_r = etree.SubElement(offer, 'param', name='Страна-производитель товара', paramid='98900')
    country_r.text = 'Египет'
    colour_r = etree.SubElement(offer, 'param', name='Основной цвет', paramid='53677')
    colour_r.text = colours
    form_r = etree.SubElement(offer, 'param', name='Форма', paramid='53667')
    form_r.text = form
    type_r = etree.SubElement(offer, 'param', name='Тип', paramid='53642')
    type_r.text = type_c
    kind_r = etree.SubElement(offer, 'param', name='Вид', paramid='243523')
    kind_r.text = 'Ковры'
    vors_r = etree.SubElement(offer, 'param', name='Высота ворса, см', paramid='53712')
    vors_r.text = pile
    material_r = etree.SubElement(offer, 'param', name='Материал', paramid='53637')
    material_r.text = material
    if len(features)>2:
        addchar_r = etree.SubElement(offer, 'param', name='Дополнительные характеристики', paramid='19596')
        addchar_r.text = 'Состав: {}'.format(features)
    design_r = etree.SubElement(offer, 'param', name='Дизайн', paramid='53672')
    design_r.text = design
    apply_r = etree.SubElement(offer, 'param', name='Назначение', paramid='126784')
    apply_r.text = apply_c


    tree = etree.ElementTree(root) 
    with open ('cleo_rztk.xml', "wb") as files :
        tree.write(files, xml_declaration=True, encoding='utf-8', pretty_print=True) 




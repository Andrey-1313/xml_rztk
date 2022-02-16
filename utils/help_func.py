import re
import os

# creating unique id for each product basen on name and size
def create_pid(collection, name, size):
	part1=str(sum(ord(i) for i in collection))
	try:
		part2=str(re.findall(r" (\d+)", name)[0])
	except:
		part2=str(sum(ord(i) for i in re.findall(r"{} ([A-Z].+)".format(collection), name)[0]))
	try:
		part3=str(ord(re.sub(r"[{} \d_]".format(collection), '', name)))
	except TypeError:
		part3=''
	part4=size.split('x')[0][:2]+size.split('x')[1][:2]

	prod_id=part1+str(part2)+part3+part4
	return prod_id

# converting product name for comparing with photo name 
def prepare_item(item):
	if item.startswith('Laos'):
		item = re.sub(r'полоска |однотон ', '', item)
	item = re.sub(r'[\s-](?!(\d|shag|small|Blue|Brown|Navy|Pink))', '_', item)
	return item

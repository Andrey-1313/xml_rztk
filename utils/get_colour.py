import os  
from PIL import Image
import csv
import re

# read csv file with rgb colors grid 
lst_csv=[]
with open('colours.csv', 'r', encoding='UTF8') as f:
    csv_f = csv.reader(f)
    header = next(csv_f)
    for name, R, G, B in csv_f:
        r=int(R)
        g=int(G)
        b=int(B)
        data=name, r, g, b
        lst_csv.append(data)

# define estimated rgb boundaries for colors
def min_max(n):
    min_n=n-15
    max_n=n+20
    return range(int(min_n), int(max_n))

# find rgb code for the matched colors sorted by repeats count
def define_rgb(rr,gg,bb,lst):
    lst_color_name=[]
    for name, r, g, b in lst:

        if rr in min_max(r) and gg in min_max(g) and bb in min_max(b):
            lst_color_name.append((name))
    return lst_color_name

# return comma separated string color names 
def main_colours(img, sensitivity='norm'):
    if sensitivity=='norm':
        n=0.2
    if sensitivity=='high':
        n=0.05
    im = Image.open(img)
    (width, height) = (im.width // 10, im.height // 10)
    im_resized = im.resize((width, height))
    counts ={}
    for ind in im_resized.getdata():

        # ignore totally white and black
        if (ind[0]+ind[1]+ind[2])<760 and (ind[0]+ind[1]+ind[2])>5:  
            for item in define_rgb(ind[0], ind[1], ind[2], lst_csv):
                colour=item
                counts[colour]=counts.get(colour, 0)+1

    for k, v in list(counts.items()):
        if v/len(im_resized.getdata())<n/len(list(counts.items())):
            counts.pop(k)
    return ','.join([name for num, name in sorted([(v, k) for k, v in counts.items()], reverse=True)])

# the main func that return photolinks and first photo color 
def photo_info(folder, item):
    data=tuple
    for direct in os.listdir(folder):
        directory=os.path.join(os.getcwd(),folder, direct)
        if os.path.isdir(directory):
            photonames=''
            filename_list=[]
            for filename in os.listdir(directory):
                sub_filename=re.sub(r'-.+', '', filename)
                # item - product name; sub_filename - photoname to compare with product
                if item==sub_filename:      
                    linkpart=re.sub(r'\.JPG','.jpg', filename)
                    linkpart=re.sub(r' ','-', filename)
                    link='https://s10.gifyu.com/images/'+linkpart
                    photonames+=link+';'
                    filename_list.append(filename)
            if len(photonames)>3:
                photonames=photonames.rstrip(';')
                # to determine the color will use main photo
                colour=main_colours(os.path.join(directory, filename_list[0]))
                if len(colour)<1:
                    colour=main_colours(os.path.join(directory, filename_list[0]), 'high')
                if len(colour.split(','))>4:
                    colour='Разноцветный,'+colour
                break
            else:
                photonames=None
                colour=None
    data=colour, photonames
    return data


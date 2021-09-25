#I'm not the original developer of the code,
# the original source can be retrieved from here:
# https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py


import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def bndBoxIndex(member):
    for index, property in enumerate(member):
        if property.tag == 'bndbox':
            return index
    return -1


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for index, member in enumerate(root.findall('object')):
            indexBndBox = bndBoxIndex(member)

            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[indexBndBox][0].text),
                     int(member[indexBndBox][1].text),
                     int(member[indexBndBox][2].text),
                     int(member[indexBndBox][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    image_path = os.path.join(os.getcwd(), 'images', 'annotations')
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv('coffee_labels.csv', index=None)
    print('Successfully converted xml to csv.')


main()

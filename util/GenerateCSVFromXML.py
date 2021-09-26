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
            index_bnd_box = bndBoxIndex(member)

            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[index_bnd_box][0].text),
                     int(member[index_bnd_box][1].text),
                     int(member[index_bnd_box][2].text),
                     int(member[index_bnd_box][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def generate_csv_from_annotations(path, path_new_file):
    image_path = os.path.join(path, 'annotations')
    images_count = [file for file in os.listdir(path) if file.endswith(".jpg") or file.endswith(".jpeg")]
    annotations_count = [file for file in os.listdir(path) if file.endswith(".xml")]
    if images_count != annotations_count:
        print("Check annotations and images files, there is a mismatch")
    else:
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(path_new_file, index=None)
        print('Successfully converted xml to csv.')


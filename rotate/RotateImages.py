import random

import cv2
import imutils
import math
import argparse
import os
import shutil
import xml.etree.ElementTree as ET
from .. import util

def rotate_point(x, y, angle, height, width):
    x = int(x)
    y = int(y)

    xCalc = math.cos(math.radians(angle)) * x - math.sin(math.radians(angle)) * y
    yCalc = math.sin(math.radians(angle)) * x + math.cos(math.radians(angle)) * y
    if xCalc < 0:
        xCalc = xCalc + height
    if yCalc < 0:
        yCalc = yCalc + width

    return [xCalc, yCalc]


def rotate_image(path, destinyPath, degree, prefix ="rotated_270_"):
    image = cv2.imread(path)
    filePath, fileName = os.path.split(path)
    newFileName = prefix + "_" + fileName
    newPath = os.path.join(destinyPath, newFileName)
    rotatedImage = imutils.rotate_bound(image, int(degree))
    cv2.imwrite(newPath, rotatedImage)
    return


def rename_xml(originalPath, newPath, imageFile):
    filePath, fileName = os.path.split(originalPath)
    try:
        shutil.copy(originalPath, newPath)
        #change xml metadata
        tree = ET.parse(newPath)
        root = tree.getroot()
        for fileNameXML in root.iter('filename'):
            fileNameXML.text = imageFile
        tree.write(newPath)
    except:
        print("Problemas procesando el archivo {0}".format(originalPath))


def modify_coordinates_xml(xmlPath, angle):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    width = 0
    height = 0
    print(xmlPath)
    angle = int(angle)
    for sizeXML in root.iter('size'):
        sizeChildren = sizeXML.getchildren()
        width = sizeChildren[0].text
        height = sizeChildren[1].text
        if angle == 90 or angle == 270:
            sizeChildren[0].text = height
            sizeChildren[1].text = width
        tree.write(xmlPath)
    for bndBoxXML in root.iter('bndbox'):
        children = bndBoxXML.getchildren()
        xmin = children[0].text
        ymin = children[1].text
        xmax = children[2].text
        ymax = children[3].text
        print("Coordenadas originales {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))
        xmin, ymin = rotate_point(xmin, ymin, angle, int(height), int(width))
        xmax, ymax = rotate_point(xmax, ymax, angle, int(height), int(width))

        if int(ymax) < int(ymin):
            print("Coordinates swapping y")
            temp = ymin
            ymin = ymax
            ymax = temp

        if int(xmax) < int(xmin):
            print("Coordinates swapping x")
            temp = xmin
            xmin = xmax
            xmax = temp


        children[0].text = str(round(xmin))
        children[1].text = str(round(ymin))
        children[2].text = str(round(xmax))
        children[3].text = str(round(ymax))

        print("Coordenadas nuevas {0} {1} {2} {3}".format(children[0].text, children[1].text, children[2].text, children[3].text))
        tree.write(xmlPath)

    return


def rotate_images(path, destiny_path, use_sample=True, sample_percentage: int = 50, degrees: list = [90, 180, 270, 360]):
    prefix_text = "rotated_"
    if not os.path.exists(path):
        raise ValueError("The source folder doesn't exist, please check the path")
    if not os.path.exists(destiny_path):
        os.makedirs(destiny_path)
    if not os.path.exists(os.path.join(destiny_path,'annotations')):
        os.makedirs(os.path.join(destiny_path,'annotations'))
    if not use_sample:
        files = [file for file in os.listdir(path) if file.endswith(".jpg") or file.endswith(".JPG")]
        files_to_process_count = len(files)
    else:
        files = [file for file in os.listdir(path) if file.endswith(".jpg") or file.endswith(".JPG")]
        files = util.PickSample.pick_sample_files_from_directory(files, 50)
        files_to_process_count = len(files)

    print("Files to process: {0}".format(files_to_process_count))
    for index, file in enumerate(files):
        file_path = os.path.join(path, file)
        print("Processing rotating image {0}".format(index + 1))
        degree = random.choice(degrees)
        rotate_image(file_path, destiny_path, degree, prefix_text)
        print("Generating new XML for image {0}".format(index + 1))
        original_xml_path = os.path.join(path, 'annotations',file.replace('.jpg','.xml').replace('.JPG','.xml'))
        new_xml_file = prefix_text + "_" + file.replace('.jpg','.xml')
        new_xml_path = os.path.join(destiny_path, 'annotations', new_xml_file)
        rename_xml(original_xml_path, new_xml_path, new_xml_file)
        modify_coordinates_xml(new_xml_path, degree)

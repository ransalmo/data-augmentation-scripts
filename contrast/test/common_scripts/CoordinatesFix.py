import argparse
import os
import shutil
import xml.etree.ElementTree as ET


def fixFilenameXML(xmlPath):
    filePath, fileName = os.path.split(xmlPath)
    # change xml metadata
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    for fileNameXML in root.iter('filename'):
        fileNameXML.text = fileNameXML.text.replace(".xml", ".jpg")
    tree.write(xmlPath)
    return


def fixCoordinatesXML(xmlPath):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    print(xmlPath)
    for bndBoxXML in root.iter('bndbox'):
        children = bndBoxXML.getchildren()
        xmin = children[0].text
        ymin = children[1].text
        xmax = children[2].text
        ymax = children[3].text
        print("Coordenadas originales {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))

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

        children[0].text = str(xmin)
        children[1].text = str(ymin)
        children[2].text = str(xmax)
        children[3].text = str(ymax)

        print("Coordenadas nuevas {0} {1} {2} {3}".format(xmin, ymin, xmax, ymax))
    tree.write(xmlPath)

    return


def fix_cordinates_xml_files(path):
    if not os.path.exists(path) or not os.path.exists(os.path.join(args.path, "annotations")):
        raise ValueError("The source folder doesn't exist or the annotations "
                         "folder does not exist, please check the path")
    files = [file for file in os.listdir(path) if file.endswith(".xml") or file.endswith(".XML")]
    files_to_process = len(files)
    print("Files to process: {0}".format(files_to_process))
    for index, file in enumerate(files):
        file_path = os.path.join(path, file)
        print("Processing rotating image {0}".format(index + 1))
        fixCoordinatesXML(file_path)


